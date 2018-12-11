import dlib
import os
from matplotlib import pyplot as plt

def face_detection(path):
	cnn_face_detector = dlib.cnn_face_detection_model_v1("../../models/mmod_human_face_detector.dat")
	win = dlib.image_window()
	for file_name in os.listdir(path):
		name, ext = file_name.split(".")
		if ext == "png":
			file_path = path+file_name
			print(file_path)
			img = dlib.load_rgb_image(file_path)

			dets = cnn_face_detector(img, 1)

			print("Number of faces detected: {}".format(len(dets)))
			for i, d in enumerate(dets):
				print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
				i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

			rects = dlib.rectangles()
			rects.extend([d.rect for d in dets])

			win.clear_overlay()
			win.set_image(img)
			win.add_overlay(rects)
			dlib.hit_enter_to_continue()
#			plt.imshow(img)
#			plt.show()


def main():
	path = "/home/welcome/Downloads/300W/01_Indoor/"
	face_detection(path)

if __name__ == "__main__":
	main()