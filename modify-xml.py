import re

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
    count = 0
    for line in file.readlines():
        count += 1
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

def main():
    in_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/labels_ibug_300W_train.xml"
    out_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/labels_ibug_300W_train_mod.xml"
    parts = "mouth"

    slice_xml(in_path, out_path, parts)

if __name__ == "__main__":
    main()