import face_recognition
import cv2
from detect_mouth_open import is_mouth_open
from datetime import datetime

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
peter_image = face_recognition.load_image_file("peter.jpg")
peter_face_encoding = face_recognition.face_encodings(peter_image)[0]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    # print('frame type:',type(frame)) # numpy.array
    # print('face_locations:',face_locations)
    # cv2.imwrite('test.png',frame) # save frame as image

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        #  See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([peter_face_encoding], face_encoding)

        name = "Unknown"
        if match[0]:
            name = "Peter"

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom), (right, bottom + 35), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom + 25), font, 1.0, (255, 255, 255), 1)


        # Display text for mouth open / close
        ret_mouth_open = is_mouth_open(frame)
        if ret_mouth_open is True:
            text = 'Mouth is open'
        elif ret_mouth_open is False:
            text = 'Open your mouth'
        else:
            text = 'Unknown'
        cv2.putText(frame, text, (left, top - 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)


    # Display the resulting image
    cv2.imshow('Video', frame)
    # print(datetime.now())

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
