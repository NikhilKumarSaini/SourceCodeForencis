import cv2 #OpenCV
import os

def preprocess_image(input_path, output_path):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    cv2.imwrite(output_path, blur)
