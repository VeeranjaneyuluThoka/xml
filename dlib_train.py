import re
import cv2
import dlib

# regex that identify the part section of the xml
REG_PART = re.compile("part name='[0-9]+'")

# regex that identify all the numbers (name, x, y) inside the part section
REG_NUM = re.compile("[0-9]+")


def slice_xml(in_path, out_path, parts):
    '''creates a new xml file stored at [out_path] with the desired landmark-points.
    The input xml [in_path] must be structured like the ibug annotation xml.'''
    file = open(in_path, "r")
    out = open(out_path, "w")
    pointSet = set(parts)

    # used to determine the part name:
    # the assumption here is that the part-indices are contigous
    index = 0

    for line in file.readlines():
        finds = re.findall(REG_PART, line)

        # find the part section
        if len(finds) <= 0:
            out.write(line)
            index = 0
        else:
            # we are inside the part section 
            # so we can find the part name and the landmark x, y coordinates
            name, x, y = re.findall(REG_NUM, line)

        # if is one of the point i'm looking for, write in the output file
        if int(name) in pointSet:
            out.write(f"      <part name='{index}' x='{x}' y='{y}'/>\n")
            index += 1

    out.close()

# define the landmark-indices we're interested to localize:
# for example if we want detect the left and right eye landmarks
LIPS = [i for i in range(48, 67)]

def train_model(name, xml):
    '''requires: the model name, and the path to the xml annotations.
    It trains and saves a new model according to the specified 
    training options and given annotations'''
    # get the training options
    options = dlib.shape_predictor_training_options()
    options.tree_depth = 4
    options.nu = 0.1
    options.cascade_depth = 15
    options.feature_pool_size = 400
    options.num_test_splits = 50
    options.oversampling_amount = 5
    #
    options.be_verbose = True  # tells what is happening during the training
    options.num_threads = 4    # number of the threads used to train the model
      
    # finally, train the model
    dlib.train_shape_predictor(xml, name, options)

def measure_model_error(model, xml_annotations):
    '''requires: the model and xml path.
    It measures the error of the model on the given
    xml file of annotations.'''
    error = dlib.test_shape_predictor(xml_annotations, model)
    print("Error of the model: {} is {}".format(model, error))
  
  
if __name__ == '__main__':
    # train a new model with a subset of the ibug annotations
    ibug_xml = "labels_ibug_300W_train.xml"
    lips_xml = "lips.xml"
    lips_dat = "lips.dat"
      
    # create the training xml for the new model with only the desired points
    slice_xml(ibug_xml, eyes_xml, parts=EYES)
      
    # finally train the eye model
    train_model(eyes_dat, eyes_xml)
      
    # ..and measure the model error on the testing annotations
    measure_model_error(eyes_dat, "labels_ibug_300W_test.xml")