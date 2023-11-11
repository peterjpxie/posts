# How to Detect Head Turn with Face Landmarks
![Featured picture](images/post_featured_picture.png)
Photo by [Prince Akachi](https://unsplash.com/@princearkman?utm_source=medium&utm_medium=referral) and [🇸🇮 Janko Ferlič](https://unsplash.com/@itfeelslikefilm?utm_source=medium&utm_medium=referral) on Unsplash

**TLDR**: When turned left, the right chin is bigger than left one, vice versa. Use the distance between the right / left chin top and the nose top to measure the right / left chin size.

I have been using bank and payment app face authentication for years where you will be asked to open mouth, turn your head etc. to authenticate you don't hack with a static photo.
I figured out [how to detect mouth open](https://medium.com/towards-data-science/how-to-detect-mouth-open-for-face-login-84ca834dff3b) years ago, but how to detect head had puzzled me for years until recently the idea came to my mind all of a sudden and it is that simple, as shown above, once you know it. Depending on the face landmanks detection library you use, you can also use this method: When turned left, you show your right ear and hide the left one, vise versa.

To start with, we will be using two Python libraries, namely `dlib` and `face_recognition`, to help detect face landmarks and analyze them to infer head orientation. 

[dlib](https://github.com/davisking/dlib) is an open source C++ library for "making real world machine learning and data analysis applications" and it is known for the production ready face detection and recognition. `dlib` also provides Python interface but `face_recognition` wraps it up in a nicer one to help you download the model file automatically and group face landmarks into facial features like eyes, nose, mouth, chin etc.

## Setting Up the Environment

Before you can detect the head turn, you'll need to have the necessary libraries installed. You'll need `dlib`, a toolkit for making real-world machine learning and data analysis applications, and `face_recognition`, a library that simplifies facial recognition processes.

Install them using pip:

```sh
pip install dlib
pip install face_recognition
```

## Understanding the Code

```python
#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont
import face_recognition
import argparse
import math

argparser = argparse.ArgumentParser("Detect head turn")
argparser.add_argument(
    "-i",
    "--image_file",
    default="left.jpg",
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
```

The provided Python code describes a simple yet effective algorithm based on facial landmarks to detect head orientation. It implies drawing lines from the top of the chin to the top of the nose and comparing their lengths to determine which direction the head is turned.

## Steps to Detect Head Turn

1. **Parse Command-Line Arguments**: Use `argparse` to provide the script with the path to the input image containing the face you want to analyze.

2. **Load and Process the Image**: Utilize the `face_recognition` library to load the image and detect the face landmarks.

3. **Calculate Distances**: Implement a function to calculate the Euclidean distance between two points. Use this to find the distances from the points at the top of the right and left chin to the top of the nose.

    Formula: `Distance = sqrt((x2 - x1)² + (y2 - y1)²)`


4. **Compare Distances**: If the distance on one side is significantly larger than on the other, conclude that the head is turned towards the shorter distance.

5. **Displaying the Result**: Use `Pillow` (PIL fork) library to draw on the image, highlighting pertinent landmarks. Add text to label the detected head orientation (turned right, turned left, facing straight).

6. **Save the Result**: Save the modified image to the disk for review.

## Running the Script

Run the script by passing the image file as an argument:

```sh
python detect_head_turn.py -i image_file.jpg
```

This command will generate an output image with the facial landmarks highlighted and the inferred head orientation labelled on the image.

## Conclusion

Facial landmark detection serves as a powerful tool for understanding more about an individual's head orientation at a given moment. By analyzing the relative sizes of the chin regions, we can accurately predict the direction of a person's head turn. Utilizing a combination of `dlib` and `face_recognition` libraries simplifies the process, allowing us to build intelligent systems that can interact with humans more naturally.