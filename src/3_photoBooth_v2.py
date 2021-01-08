import os
import cv2

WORKSPACE = "../"
DATA_DIR = WORKSPACE + "dataset/"
MODELS_DIR = WORKSPACE + "models/"

nb_img = 0
photoTook = 0

tips = False
record = False

frameWidth = 640
frameHeight = 480

cascade = MODELS_DIR + "haarcascade_frontalface_alt2.xml"

name = str(input("\n[?] - What is your dataset's name?\n > "))
filename = DATA_DIR + name

try:
    os.mkdir(DATA_DIR)
except:
    pass

try:
    os.mkdir(DATA_DIR + name)
except:
    pass

print("\n[!] - Start capturing...")

# Start camera and create a VideoCapture Object
# 0: built-in camera
# 1, 2, ...: are other(s) camera(s) connected by usb)
camera = cv2.VideoCapture(0)

# Setting openCV window dimension (640 width * 480 height in pixels)
camera.set(3, frameWidth)
camera.set(4, frameHeight)

# Main loop app where image will be displayed in a window
while True:
    faceDetected = False

    

    # Read each image of the video (frame per frame)
    _, frame = camera.read()

    if not _:
        print("[X] - Failed to take photo")
        break

    # Create a Cascade classifier object
    detectorModel = cv2.CascadeClassifier(cascade)

    # Convert initial image in gray (better result)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Search the coordinate of the face in image
    faces = detectorModel.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(70, 70))

    # Draw a red rectangle on recognized face
    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faceDetected = True
        # print("Face detected!")
    cv2.putText(frame, 
                "Faces: {}".format(str(len(faces))), (5, 30), 
                cv2.FONT_HERSHEY_PLAIN, 2, 
                (255, 0, 0), 2)

    # COMMANDS HUD
    cv2.rectangle(frame, (0, 0), (frameWidth, 30), (100, 100, 100), cv2.FILLED)
    cv2.putText(frame, "[ESC] Quit", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "Face(s):", (110, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "{}".format(str(len(faces))), (180, 22), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 0, 255), 0)
    cv2.putText(frame, "[H] Help", (206, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "Photos:", (285, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "{}".format(str(photoTook)), (350, 22), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 255, 0), 0)
    cv2.putText(frame, "[spacebar] Take photos", (frameWidth - 235, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)

    if faceDetected:
        cv2.putText(frame, 
                    "FACE DETECTED!", (200, 65), 
                    cv2.FONT_HERSHEY_PLAIN, 2, 
                    (0, 255, 0), 2)

        if record == True:
            cv2.circle(frame, (frameWidth - 20, 15), 5, (0, 0, 255), 8)
            cv2.imwrite(filename + "/image_{}.png".format(nb_img), frame[y:y+h, x:x+w])
            nb_img += 1
            photoTook += 1

    # Help HUD
    if tips:
        cv2.rectangle(frame, (275, 325), (50, 50), (100, 100, 100), cv2.FILLED)
        cv2.rectangle(frame, (275, 325), (50, 50), (0, 0, 0), 1)
        cv2.putText(frame, "[F] Force photo.", (60, 75), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, "Take photo in diff. pos:", (60, 125), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - Up / Down.", (60, 150), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - Left / Right.", (60, 175), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - Front.", (60, 200), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - Glasses / or not.", (60, 225), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - Eyes open / closed.", (60, 250), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - A bit of rotation.", (60, 275), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
        cv2.putText(frame, " - ...", (60, 300), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)

    # Display this image on the screen
    cv2.imshow(" Capturing - {}".format(str(name)), frame)

    # Wait until key button is pressed
    key = cv2.waitKey(1) & 0xFF

    # Press ESCAPE to stop app (ASCII code decimal = 27)
    if key == 27:
        print("\n > [+] {} Photos have been saved in \"".format(str(photoTook)) + filename + "/\" directory.\n")
        print("[!] - Stop capturing!", "\n")
        break

    # Space bar to take photos (until button is pressed)
    if key == 32:
        record=not record
    
    # TODO
    # Force taking photo even face is not detected
    if key == ord("f"):
        if not tips:
            cv2.imwrite(filename + "/image_{}.png".format(nb_img), frame[y:y+h, x:x+w])
            nb_img += 1
            photoTook += 1

    # TODO
    # Display shortcut (help)
    if key == ord("h"):
        tips=not tips

    # TODO
    # Faire la détection du profile gauche et droit.

# Release camera to other software
camera.release()
cv2.destroyAllWindows()
