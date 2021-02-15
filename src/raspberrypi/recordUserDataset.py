import cv2
import time
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from src.variables.global_variables import *


def photoBooth_raspberry():
    nb_img = 0
    photoTook = 0

    tips = False
    record = False

    frameWidth = 640
    frameHeight = 480

    name = str(input("\n[?] - What is your dataset's name?\n > "))
    filename = DATA_DIR + name

    # Create folder if they doesn't exist yet
    try:
        os.mkdir(DATA_DIR)
    except:
        pass

    try:
        os.mkdir(DATA_DIR + name)
    except:
        pass

    print("\n[!] - Start capturing...")

    # Initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (frameWidth, frameHeight)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(frameWidth, frameHeight))

    # Allow the camera to warmup
    time.sleep(0.1)

    # Main loop app
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # Main loop app where image will be displayed in a window
        while True:
            faceDetected = False

            # Create a Cascade classifier object
            detectorModel = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

            # Convert initial image in gray (better result)
            gray_frame = cv2.cvtColor(cv2.UMat(frame.array), cv2.COLOR_BGR2GRAY)

            # Search the coordinate of the face in image
            faces = detectorModel.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(70, 70))

            # Draw a red rectangle on recognized face
            for x, y, w, h in faces:
                frame = cv2.rectangle(frame.array, (x, y), (x + w, y + h), (0, 0, 255), 2)
                faceDetected = True
                # print("Face detected!")

            # COMMANDS HUD
            cv2.rectangle(frame.array, (0, 0), (frameWidth, 30), (100, 100, 100), cv2.FILLED)
            cv2.putText(frame.array, "[ESC] Quit", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
            cv2.putText(frame.array, "Face(s):", (110, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
            cv2.putText(frame.array, "{}".format(str(len(faces))), (180, 22), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 0, 255), 0)
            cv2.putText(frame.array, "[H] Help", (206, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
            cv2.putText(frame.array, "Photos:", (285, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
            cv2.putText(frame.array, "{}".format(str(photoTook)), (350, 22), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 255, 0), 0)
            cv2.putText(frame.array, "[spacebar] Take photos", (frameWidth - 235, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)

            if faceDetected:
                cv2.putText(frame.array, 
                            "FACE DETECTED!", (200, 65), 
                            cv2.FONT_HERSHEY_PLAIN, 2, 
                            (0, 255, 0), 2)

                if record:
                    cv2.circle(frame.array, (frameWidth - 20, 15), 5, (0, 0, 255), 8)
                    cv2.imwrite(filename + "/image_{}.png".format(nb_img), frame.array[y:y+h, x:x+w])
                    nb_img += 1
                    photoTook += 1

            # Help HUD
            if tips:
                cv2.rectangle(frame.array, (275, 350), (50, 50), (100, 100, 100), cv2.FILLED)
                cv2.rectangle(frame.array, (275, 350), (50, 50), (0, 0, 0), 1)
                cv2.putText(frame.array, "[F] Force photo.", (60, 75), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, "[H] Close help.", (60, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, "Take photo in diff. pos:", (60, 150), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - Up / Down.", (60, 175), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - Left / Right.", (60, 200), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - Front.", (60, 225), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - Glasses / or not.", (60, 250), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - Eyes open / closed.", (60, 275), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - A bit of rotation.", (60, 300), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
                cv2.putText(frame.array, " - ...", (60, 325), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)

            # Display frame in openCV window
            cv2.imshow(" Capturing - {}".format(str(name)), frame.array)

            if spaceBetweenFrame:
                for i in range(nb_frameBeforeNextPhoto):
                    frame = camera.read()

            # Wait until key button is pressed
            key = cv2.waitKey(1) & 0xFF

            # Press ESCAPE to stop app (ASCII code decimal = 27)
            if key == 27:
                print("\n > [+] {} Photos have been saved in \"".format(str(photoTook)) + filename + "/\" directory.\n")
                print("[!] - Stop capturing!", "\n")
                break

            # Press SPACEBAR to take photos (press button again to stop taking photo)
            # Take 1 photo per frame per seconds (~ 60 photos / second if you have a good PC)
            if key == 32:
                record=not record
            
            # Press F to force taking photo even face is not detected
            if key == ord("f"):
                if not tips: # We don't force taking photo if help are displayed on screen
                    cv2.imwrite(filename + "/image_{}.png".format(nb_img), frame.array[y:y+h, x:x+w])
                    nb_img += 1
                    photoTook += 1

            # Display shortcuts (help)
            if key == ord("h"):
                tips=not tips
        
        rawCapture.truncate(0)
