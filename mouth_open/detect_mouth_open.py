import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw
import face_recognition
import ipdb

def add_index(ax,text,x,y,v_offset=3,color='black'):
    ax.annotate(text,
                xy=(x, y),
                xytext=(0, v_offset),  # 3 points vertical offset
                textcoords='offset points',
                ha='center', # ha = 'left',
                va='bottom',
                color=color
               )

# annotate height line
def draw_line(ax,x1,y1,x2,y2,color='black'):
    ax.annotate('', # empty text
                xy=(x1, y1),
                xytext=(x2, y2),
                ha='center', # ha = 'left',
                va='bottom',
                arrowprops=dict(edgecolor=color,arrowstyle="<->",linestyle='--') # facecolor=color,
               )

def get_lip_height(lip):
    sum=0
    for i in [2,3,4]:
        # distance of two near points up and down
        distance = math.sqrt( (lip[i][0] - lip[12-i][0])**2 + (lip[i][1] - lip[12-i][1])**2 )
        sum += distance
    return sum / 3

def get_mouth_height(top_lip,bottom_lip):
    sum=0
    for i in [8,9,10]:
        # distance of two near points up and down
        distance = math.sqrt( (top_lip[i][0] - bottom_lip[18-i][0])**2 + (top_lip[i][1] - bottom_lip[18-i][1])**2 )
        sum += distance
    return sum / 3

def is_mouth_open(image):
    """
    image is numpy array
    """
    # Find all facial features in all the faces in the image
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_num = len(face_landmarks_list)
    print("I found {} face(s) in this photograph.".format(face_num))

    if face_num != 1:
        return None

    # if there is only one face in the image
    face_landmarks = face_landmarks_list[0]
    # facial_features = [
    #     'top_lip',
    #     'bottom_lip'
    # ]
    top_lip = face_landmarks['top_lip']
    bottom_lip = face_landmarks['bottom_lip']
    top_lip_height = get_lip_height(top_lip)
    bottom_lip_height = get_lip_height(bottom_lip)
    mouth_height = get_mouth_height(top_lip, bottom_lip)
    # if mouth is open more than lip height, return true.
    if mouth_height > min(top_lip_height, bottom_lip_height) / 2:
        return True
    else:
        return False

    # for facial_feature in facial_features:
    #    print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

        # Let's trace out each facial feature in the image with a line!
        # for facial_feature in facial_features:
        #     d.line(face_landmarks[facial_feature], width=5)



def main():
    # close mouth
    # top_lip = [(151, 127), (157, 126), (163, 126), (168, 127), (172, 127), (178, 127), (185, 129), (182, 129), (172, 130), (167, 130), (163, 129), (153, 127)]
    # bottom_lip = [(185, 129), (177, 133), (171, 135), (166, 135), (161, 134), (156, 132), (151, 127), (153, 127), (162, 129), (167, 130), (171, 130), (182, 129)]

    # obama open mouth
    top_lip = [(181, 359), (192, 339), (211, 332), (225, 336), (243, 333), (271, 342), (291, 364), (282, 363), (242, 346), (225, 347), (211, 345), (188, 358)]
    bottom_lip = [(291, 364), (270, 389), (243, 401), (223, 403), (207, 399), (190, 383), (181, 359), (188, 358), (210, 377), (225, 381), (243, 380), (282, 363)]

    # top_lip = [(140, 221), (148, 218), (157, 216), (164, 218), (171, 216), (179, 217), (187, 220), (184, 221), (171, 220), (164, 221), (157, 220), (143, 222)]
    # bottom_lip = [(187, 220), (179, 231), (171, 236), (164, 237), (156, 236), (147, 230), (140, 221), (143, 222), (156, 229), (164, 230), (171, 229), (184, 221)]

    x1 = [ x for x,y in top_lip]
    y1 = [ y for x,y in top_lip]
    x2 = [ x for x,y in bottom_lip]
    y2 = [ y for x,y in bottom_lip]
    n1=0
    m1=12
    n2=0
    m2=12

    fig, ax = plt.subplots()
    # fig, ax = plt.subplots(figsize=(8,6))
    # ax.plot(x1, y1,color='black', marker='.')
    # ax.plot(x2, y2,color='black', marker='.')
    ax.plot(x1[n1:m1], y1[n1:m1],color='green', marker='o')
    ax.plot(x2[n2:m2], y2[n2:m2],color='blue', marker='*')

    plt.gca().invert_yaxis()

    # add index number for top lip
    for i in range(12):
        x = top_lip[i][0]
        y = top_lip[i][1]
        add_index(ax,str(i),x,y,color='green',v_offset=5)

    # add index number for bottom lip
    for i in range(12):
        x = bottom_lip[i][0]
        y = bottom_lip[i][1]
        add_index(ax,str(i),x,y,color='blue',v_offset=-20)

    # draw line top lip
    for i in [2,3,4]:
        x1 = top_lip[i][0]
        y1 = top_lip[i][1]
        x2 = top_lip[12-i][0]
        y2 = top_lip[12-i][1]
        draw_line(ax,x1,y1,x2,y2,color='green')

    # draw line bottom lip
    for i in [2,3,4]:
        x1 = bottom_lip[i][0]
        y1 = bottom_lip[i][1]
        x2 = bottom_lip[12-i][0]
        y2 = bottom_lip[12-i][1]
        draw_line(ax,x1,y1,x2,y2,color='blue')

    # draw line mouth
    for i in [8,9,10]:
        x1 = top_lip[i][0]
        y1 = top_lip[i][1]
        x2 = bottom_lip[18-i][0]
        y2 = bottom_lip[18-i][1]
        draw_line(ax,x1,y1,x2,y2,color='black')

    # annotate height
    # top lip height
    x = (top_lip[4][0] + top_lip[8][0])/2
    y = (top_lip[4][1] + top_lip[8][1])/2
    ax.annotate('lip height',
                xy=(x, y), xytext=(5,0), textcoords='offset points',
                ha='left', va='top',color='green'
               )

    # bottom lip height
    x = (bottom_lip[2][0] + bottom_lip[10][0])/2
    y = (bottom_lip[2][1] + bottom_lip[10][1])/2
    ax.annotate('lip height',
                xy=(x, y), xytext=(5,0), textcoords='offset points',
                ha='left', va='bottom',color='blue'
               )

    # mouth height
    x = (top_lip[8][0] + bottom_lip[10][0])/2
    y = (top_lip[8][1] + bottom_lip[10][1])/2
    ax.annotate('mouth height',
                xy=(x, y), xytext=(5,0), textcoords='offset points',
                ha='left', va='bottom',color='black'
               )

    plt.show()
    # fig.savefig("test.png")
    # plt.savefig("test.png",format='png') # savefig() will show figure on jupyter as well.

    print('top_lip height:', lip_height(top_lip))
    print('bottom_lip height:',lip_height(bottom_lip))
    print('mouth height:',mouth_height(top_lip,bottom_lip))

def main2():
    image = face_recognition.load_image_file("obama3.jpg")
    print('mouth open: %s' % is_mouth_open(image))

if __name__ == '__main__':
    # main()
    main2()
