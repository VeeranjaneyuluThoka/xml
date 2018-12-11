import os
import cv2
from matplotlib import pyplot as plt
import dlib

def parse_ptf_files(file_names_list, landmarks_list):
#    cascade = cv2.CascadeClassifier("../DeepAlignmentNetwork-master/data/haarcascade_frontalface_alt.xml")

    for (pts_file,png_file) in zip(landmarks_list, file_names_list):
        
        f = open(pts_file, 'r')
        data = f.readlines()
        
        bgr_img = cv2.imread(png_file)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        #res_img = cv2.resize(bgr_img, (1920,1080))
        
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
#        rects = cascade.detectMultiScale(bgr_img, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50))
#        for (x, y, w, h) in rects:
#            cv2.rectangle(rgb_img, (x,y), (x+w, y+h), (255,0,0), 2)
        cv2.imshow(png_file, bgr_img)
        cv2.waitKey(0)

def list_files_dispaly_with_landmarks(path):
    file_names_list = []
    landmarks_list = []
    for file_name in os.listdir(path):
        name, ext = file_name.split(".")
        png_file_path = path+file_name
        pts_file_path = path+name+'.pts'
        if ext == 'png':
            file_names_list.append(png_file_path)
            landmarks_list.append(pts_file_path)
     
    #detect face in an image
    #detect_face(file_names_list)
    
    #parse ptf files and apply landmarks on face
    parse_ptf_files(file_names_list, landmarks_list)

def main():
	path = "/home/welcome/Downloads/VM/data/ibug_300W_large_face_landmark_dataset/300W/01_Indoor/"
	list_files_dispaly_with_landmarks(path)

if __name__ == "__main__":
	main()