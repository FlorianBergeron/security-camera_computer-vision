import cv2

# Directory paths
WORKSPACE = "../"
MODELS_DIR = WORKSPACE + "models/"
HAARSCASCADE_MODELS_DIR = MODELS_DIR + "haarscascade/"

# Variables
frameWidth = 640
frameHeight = 480
cascade = HAARSCASCADE_MODELS_DIR + "haarcascade_frontalface_alt2.xml"

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
    faces = detectorModel.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=3)

    # Draw a red rectangle on recognized face
    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        faceDetected = True
        # print("Face detected!")

    cv2.putText(frame, 
                "Faces: {}".format(str(len(faces))), (5, 30), 
                cv2.FONT_HERSHEY_PLAIN, 2, 
                (255, 0, 0), 2)

    if faceDetected == True:
        cv2.putText(frame, 
                    "FACE DETECTED!", (200, 75), 
                    cv2.FONT_HERSHEY_PLAIN, 2, 
                    (0, 255, 0), 2)

    # Display this image on the screen
    cv2.imshow(" Capturing - Press ESC to quit", frame)

    # Wait until key button is pressed
    key = cv2.waitKey(1) & 0xFF
    
    # Press ESCAPE to stop app (ASCII code decimal = 27)
    if key == 27:
        print("[!] - Stop capturing!", "\n")
        break

# Release camera to other software
camera.release()
cv2.destroyAllWindows()
