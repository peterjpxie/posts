#!/usr/bin/env python
from PIL import Image
import face_recognition # 2.5s to import, I think loading the model takes time
import argparse

argparser = argparse.ArgumentParser(description="find faces in picture")
argparser.add_argument(
    "image_file",
    # nargs="?",
    # default="left.jpg",
    help="Image file to detect head turn",
)
args = argparser.parse_args()

image_file = args.image_file

# image_file='left.jpg'
# Load the jpg file into a numpy array
image = face_recognition.load_image_file(image_file)

# Find all the faces in the image
face_locations = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    # pil_image.show()
