#!/usr/bin/env python
"""
Detect head turn with dlib and face_recognition

Algorithm: When turned left, the right chin is bigger than left one, vice versa.
Use the distance between the right / left chin top and the nose top to measure the right / left chin size.

Usage: python detect_head_turn.py -i image_file
"""
from PIL import Image, ImageDraw, ImageFont
import face_recognition
import argparse
import math

argparser = argparse.ArgumentParser(description="Detect head turn")
argparser.add_argument(
    "image_file",
    # nargs="?",
    # default="left.jpg",
    help="Image file to detect head turn",
)
args = argparser.parse_args()

image_file = args.image_file

# Load the jpg file into a numpy array
image = face_recognition.load_image_file(image_file)

# Find face landmarks of all the faces in the image
face_landmarks_list = face_recognition.face_landmarks(image)
num_faces = len(face_landmarks_list)
print(f"Found {num_faces} face(s) in this photograph.")
# Get locations of all the faces in the image
face_locations = face_recognition.face_locations(image)

pil_image = Image.fromarray(image)
d = ImageDraw.Draw(pil_image)

facial_features = [
    "chin",
    "left_eyebrow",
    "right_eyebrow",
    "nose_bridge",
    "nose_tip",
    "left_eye",
    "right_eye",
    "top_lip",
    "bottom_lip",
]

def point_distance(p1,p2):
    """get distance of two points"""
    return math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )

# get landmarks of first face, assume there is only one face in the image
face_landmarks = face_landmarks_list[0]
# Let's trace out each facial feature in the image with a line!
for facial_feature in facial_features:
    # print(f"{facial_feature} has {len(face_landmarks[facial_feature])} points: {face_landmarks[facial_feature]}")
    d.line(face_landmarks[facial_feature], width=5)

# draw left chin to nose top in green
d.line(face_landmarks["chin"][-1:] + face_landmarks["nose_bridge"][:1], width=5, fill=(0, 255, 0))
# draw right chin to nose top in red
d.line(face_landmarks["chin"][:1] + face_landmarks["nose_bridge"][:1], width=5, fill=(255, 0, 0))

# right / left chin ratio
left_chin_green = point_distance(face_landmarks["chin"][-1], face_landmarks["nose_bridge"][0])
right_chin_red = point_distance(face_landmarks["chin"][0], face_landmarks["nose_bridge"][0])
right_to_left_ratio = right_chin_red / left_chin_green
left_to_right_ratio = left_chin_green / right_chin_red

## Add the text to the image
threshold = 1.3
if left_to_right_ratio > threshold:
    turned = "turned right"
    print(f"green / red = {left_to_right_ratio:.1f}, {turned}")
elif right_to_left_ratio > threshold:
    turned = "turned left"
    print(f"red / green = {right_to_left_ratio:.1f}, {turned}")
else:
    turned = "facing straight"
    print(f"red / green = {right_to_left_ratio:.1f}, {turned}")

top, right, bottom, left = face_locations[0]
position = (left, top)
font_size = (right - left) // 6 # relative to face size
font = ImageFont.truetype("arial.ttf", size=font_size)
text_color = (0, 0, 255)  # RGB color
d.text(position, turned, fill=text_color, font=font)

# Save drawn image
out_file = "out_" + image_file
print("saved to " + out_file)
pil_image.save(out_file)
# pil_image.show()
