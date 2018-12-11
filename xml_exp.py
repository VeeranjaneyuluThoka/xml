from xml.dom import minidom
import xml.etree.ElementTree as ET
import cv2
import os

def read_xml_using_minidom(path):
	mydoc = minidom.parse(path)
	images = mydoc.getElementsByTagName('image')

	count = 0
	for ind in range(len(images)):
		print(images[ind].attributes['file'].value)
		count += 1
	print(count)

def read_xml_using_element_tree(path):
#	print("Veeru:",path)
	tree = ET.parse(path)
	root = tree.getroot()

	for elem in root:
		for img_subelem in elem:
			try:
				file_path = img_subelem.attrib.get('file')
#				print(file_path)
				img = cv2.imread(file_path)
#				cv2.imshow("org", img)
#				cv2.waitKey(0)
				for box_subelem in img_subelem:
					x = box_subelem.attrib.get('left')
					y = box_subelem.attrib.get('top')
					w = box_subelem.attrib.get('width')
					h = box_subelem.attrib.get('height')
					px=int(x)
					py = int(y)
					pw = int(w)
					ph = int(h)
					cv2.rectangle(img, (px,py), (px+pw, py+ph), (255,0,0), 2)

					for part_subelem in box_subelem:
						name = part_subelem.attrib.get('name')
						num = int(name)
						if num < 48:
							continue
						x = part_subelem.attrib.get('x')
						y = part_subelem.attrib.get('y')

						#float string
						px = int(float(x))
						py = int(float(y))
						#print(px, py)
						cv2.circle(img, (px, py), 2, (0, 255, 0))

				cv2.imshow("rects", img)
				cv2.waitKey(0)
			except:
				pass

def write_data_into_xml_elementtree(path):
	images = ET.Element('images')
	image = ET.SubElement(images, 'image')
	box = ET.SubElement(image, 'box')
	part = ET.SubElement(box, 'part')

	mydata = ET.tostring(images)
	print(type(mydata))
	myfile = open(path, 'wb')
	myfile.write(mydata)

def prettify(elem):
	"""
	Return a pretty-printed XML string for the Element.
	"""
	rough_string = ET.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")

def create_dlib_format(dpath):

	data = ET.Element("dataset")
	images = ET.SubElement(data, 'images')

	image = ET.SubElement(images, 'image')
	image.set('file', 'file_path')
	box = ET.SubElement(image, 'box')
	box.set('top', '10')
	box.set('left','20')
	box.set('width','30')
	box.set('height','40')
	part = ET.SubElement(box, 'part')
	for i in range(60):
		part.set('name', str(i))
		part.set('x', '20')
		part.set('y', '30')

	root = prettify(data)
	print(root)

def mod_xml_element_tree(path, mpath):
	root = ET.parse(path).getroot()
	images = root.find('images')

	for image in images.findall('image'):
		box = image.find('box')
		if box.attrib.get('left') == None:
			images.remove(image)

	tree = ET.ElementTree(root)
	with open(mpath, 'wb') as fh:
		tree.write(fh)

def rename_files_xml(path, mpath):
	root = ET.parse(path).getroot()
	images = root.find('images')

	npath = "/home/welcome/Downloads/VM/data/inhouse_data/frames_DAN_Ruchi/"
	for image in images.findall('image'):
		file_name = image.attrib.get('file')
		path, fname = os.path.split(file_name)
		file_path = npath+fname
		image.set('file', file_path)

	tree = ET.ElementTree(root)
	with open(mpath, 'wb') as fh:
		tree.write(fh)

def update_xml_file(sPath, nPath, mfile):
	sroot = ET.parse(sPath).getroot()
	simages = sroot.find('images')

	nroot = ET.parse(nPath).getroot()
	nimages = nroot.find('images')

	for nimage in nimages.findall('image'):
		for simage in simages.findall('image'):
			if simage.attrib.get('file') == nimage.attrib.get('file'):
				sbox = simage.find('box')
				nbox = nimage.find('box')
				sbox.set('left', nbox.attrib.get('left'))
				sbox.set('top', nbox.attrib.get('top'))
				sbox.set('width', nbox.attrib.get('width'))
				sbox.set('height', nbox.attrib.get('height'))

	tree = ET.ElementTree(sroot)
	with open(mfile, 'wb') as fh:
		tree.write(fh)

def merge_files(files, dest_path):
	first = None
	for filename in files:
		data = ET.parse(filename).getroot()
		if first is None:
			first = data
		else:
			first.extend(data)

#    if first is not None:
#        print(ET.tostring(first))

	tree = ET.ElementTree(first)
	with open(dest_path, 'wb') as fh:
		tree.write(fh)

def parse_ptf_files(file_names_list, landmarks_list, marked_path):

    for (pts_file,png_file) in zip(landmarks_list, file_names_list):
        
        f = open(pts_file, 'r')
        data = f.readlines()
        
        bgr_img = cv2.imread(png_file)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        
        for x in data:
            if x.strip() == 'version: 1':
                continue
            elif x.strip() == 'n_points: 68':
                continue
            elif x.strip() == '{':
                continue
            elif x.strip() == '}':
                continue
            else:                    
                x, y = x.strip().split(' ')
                px = int(float(x))
                py = int(float(y))
                cv2.circle(bgr_img, (px, py), 2, (0, 255, 0), 2)

        pdir, fname = os.path.split(png_file)
        dst_path = marked_path+fname
        print(dst_path)
        cv2.imwrite(dst_path, bgr_img)

#        cv2.imshow(png_file, bgr_img)
#        cv2.waitKey(0)

def list_files_dispaly_with_landmarks(path, marked_path):
    file_names_list = []
    landmarks_list = []
    for file_name in os.listdir(path):
        name, ext = file_name.split(".")
        png_file_path = path+file_name
        pts_file_path = path+name+'.pts'
        if ext == 'png':
            file_names_list.append(png_file_path)
            landmarks_list.append(pts_file_path)
     
    parse_ptf_files(file_names_list, landmarks_list, marked_path)
    #return landmarks_list

def merge_fd_box_landmarks(mfile, ptf_path, dst_file_path):
	root = ET.parse(mfile).getroot()
	images = root.find('images')

	for image in images.findall('image'):
		file_name = image.attrib.get('file')
		pdir, fname = os.path.split(file_name)
		name, ext = fname.split('.')
		ptf_name = name+'.pts'
		pts_path = ptf_path+ptf_name

		box = image.find('box')

		f = open(pts_path, 'r')
		data = f.readlines()
             
		count = 0
		for x in data:
			if x.strip() == 'version: 1':
				continue
			elif x.strip() == 'n_points: 68':
				continue
			elif x.strip() == '{':
				continue
			elif x.strip() == '}':
				continue
			else:
				part = ET.SubElement(box, 'part')
				x, y = x.strip().split(' ')
				px = int(float(x))
				py = int(float(y))
				part.set('name', str(count))
				part.set('x', str(px))
				part.set('y', str(py))
				count += 1

	#print(ET.tostring(root))
	tree = ET.ElementTree(root)
	with open(dst_file_path, 'wb') as fh:
		tree.write(fh)

def replace_string():
	old_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300W/01_Indoor/indoor_001.png"
	old_string = '/home/welcome/Downloads/VM'
	new_string = "/nfs/data/Veeru/VM/DL_methods"

	print(old_path.replace(old_string, new_string))

def replace_files_path_in_xml_files(xml_file_path, xml_gpu_file_path):
	root = ET.parse(xml_file_path).getroot()
	#images = root.find('images')

	old_string = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300W'
	new_string = '300W'

	#old_string = '/home/welcome/Downloads/VM/data/inhouse_data'
	#new_string = 'inhouse_data'
	for images in root.findall('images'):
		for image in images.findall('image'):
			file_name = image.attrib.get('file')
			#print(file_name)
			new_file_name=file_name.replace(old_string, new_string)
			image.set('file', new_file_name)

	tree = ET.ElementTree(root)
	with open(xml_gpu_file_path, 'wb') as fh:
		tree.write(fh)

def main():
	#replace_string()

	rpath = '../../data/ibug_300W_large_face_landmark_dataset/labels_ibug_300W.xml'
	wpath = '../../data/ibug_300W_large_face_landmark_dataset/labels_exp.xml'

	dpath = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/dlib_exp_ruchi_mod.xml'
	mpath = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/dlib_exp_veeru.xml'

	sPath = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/dlib_exp_ruchi.xml'
	nPath = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/fd_ruchi.xml'
#	mfile = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/dlib_exp_ruchi_box_updated.xml'
	mfile = '/home/welcome/Downloads/dlib-19.16/tools/imglab/build/fd_300w_indoor'

	files = []
	dest_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300w_indoor_inhouse_ibug_300w_train.xml"

	dst_file_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_corrected_files/300w_indoor.xml"

	"""
	data_path_300w = '../../data/ibug_300W_large_face_landmark_dataset/300W/02_Outdoor/'
	marked_files_path_300w = '../../data/ibug_300W_large_face_landmark_dataset/300W/02_Outdoor_marked/'
	list_files_dispaly_with_landmarks(data_path_300w, marked_files_path_300w)"""

	"""
	#merge all xml files present in a folder
	xml_files_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/merge_all/"
	for filename in os.listdir(xml_files_path):
		comp_path = xml_files_path+filename
		files.append(comp_path)
	merge_files(files, dest_path)"""

#	update_xml_file(sPath, nPath, mfile)

#	rename_files_xml(dpath, mpath)

#	read_xml_using_minidom(rpath)

	file_path = "../../data/ibug_300W_large_face_landmark_dataset/labels_ibug_300W_train.xml"
	read_xml_using_element_tree(file_path)
	
#	mod_xml_element_tree(dpath, mpath)

#	write_data_into_xml_elementtree(wpath)
	
#	create_dlib_format(dpath)

	"""
	#replace file paths with new paths
	#xml_file_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_files/gpu_xml_files/300w_indoor.xml"
	#xml_gpu_file_path = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/xml_files/gpu_xml_files/300w_indoor_gpu.xml'

	xml_file_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300w_indoor.xml"
	xml_gpu_file_path = '/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300w_indoor_gen_path.xml'

	replace_files_path_in_xml_files(xml_file_path, xml_gpu_file_path)"""

	#ptf_path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300W/01_Indoor/"
	#merge_fdbox_landmarks(mfile, ptf_path, dst_file_path)

if __name__ == "__main__":
	main()