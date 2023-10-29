#!/usr/bin/python
"""
Use only dlib
#   You can get the trained model file from:
#   http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2.
#   Note that the license for the iBUG 300-W dataset excludes commercial use.
#   So you should contact Imperial College London to find out if it's OK for
#   you to use this model file in a commercial product.
"""
#%%
import sys
import os
import dlib
import argparse

# argparser = argparse.ArgumentParser('Find facial landmarks')
# argparser.add_argument('-i', '--image_file', default='obama.jpg', help='Image file to find facial landmarks')
# args = argparser.parse_args()

image_file = 'obama.jpg' # args.image_file

predictor_path = 'shape_predictor_68_face_landmarks.dat' # sys.argv[1]

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
win = dlib.image_window()

print("Processing file: {}".format(image_file))
img = dlib.load_rgb_image(image_file)

win.clear_overlay()
win.set_image(img)

# Ask the detector to find the bounding boxes of each face. The 1 in the
# second argument indicates that we should upsample the image 1 time. This
# will make everything bigger and allow us to detect more faces.
dets = detector(img, 1)
print("Number of faces detected: {}".format(len(dets)))
for k, d in enumerate(dets):
    print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        k, d.left(), d.top(), d.right(), d.bottom()))
    # Get the landmarks/parts for the face in box d.
    shape = predictor(img, d)
#%%    
    print("Detect %s landmarks points %s." % (shape.num_parts, shape.parts()))
    ''' OUT
    # face_recognition package categorize these points into features, like chin, eye, nose, mouth, etc.
    Detection 0: Left: 502 Top: 354 Right: 1167 Bottom: 1020
    Detect 68 landmarks points points[(485, 560), (491, 647), (499, 736), (517, 823), (547, 907), (595, 983), (656, 1050), (728, 1101), (815, 1112), (904, 1092), (975, 1035), (1037, 964), (1085, 887), (1111, 806), (1125, 722), (1130, 639), (1131, 560), (554, 528), (593, 480), (651, 459), (714, 460), (776, 475), (868, 475), (926, 457), (989, 455), (1048, 478), (1083, 524), (821, 531), (821, 587), (821, 643), (821, 703), (738, 734), (778, 744), (820, 754), (862, 742), (903, 730), (628, 551), (662, 533), (698, 530), (735, 550), (698, 554), (662, 556), (907, 548), (943, 528), (980, 530), (1016, 549), (980, 554), (943, 552), (656, 832), (708, 810), (773, 804), 
    (819, 811), (863, 801), (926, 805), (981, 823), (930, 891), (868, 926), (821, 932), (772, 928), (709, 899), (671, 835), (773, 824), (819, 830), (864, 822), (964, 827), (866, 884), (820, 892), (773, 886)].
    '''
    # Draw the face landmarks on the screen.
    win.add_overlay(shape)

win.add_overlay(dets)
# dlib.hit_enter_to_continue()