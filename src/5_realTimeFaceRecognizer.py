import cv2
import pickle
import numpy as np

# import 4_trainLBPHFaceRecognizer

WORKSPACE = "../"
DATA_DIR = WORKSPACE + "dataset/"
MODELS_DIR = WORKSPACE + "models/"
LBFH_MODELS_DIR = WORKSPACE + "models/LBFH/"
MODELS_DATA_DIR = LBFH_MODELS_DIR + "data/"
HAARSCASCADE_MODELS_DIR = MODELS_DIR + "haarscascade/"

id_image=0
frameWidth = 640
frameHeight = 480
userColorGranted = (0, 255, 0)
userColorUnknown = (0, 0, 255)
userColorInfo = (255, 255, 255)
threshold_confidence_index = 100

intrusion = False
sendAlert = False
nb_intrusion = 0
nb_intrusion_total = 0

cascade = HAARSCASCADE_MODELS_DIR + "haarcascade_frontalface_alt2.xml"
detectorModel = cv2.CascadeClassifier(cascade)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(LBFH_MODELS_DIR + "custom_LBFHFaceRecognizer_model.yml")

print("\n[!] - Open user's data for recognition.")
with open(MODELS_DATA_DIR + "data_custom_LBFHFaceRecognizer_model.pickle", "rb") as f:
    data = pickle.load(f)
    labels = {v:k for k, v in data.items()}

print("[!] - Start capturing...")
camera = cv2.VideoCapture(0)

camera.set(3, frameWidth)
camera.set(4, frameHeight)

while True:
    intrusion = False

    _, frame = camera.read()

    # Check if python can get frame from camera
    if not _:
        print("[X] - Failed to read frame from camera!")
        break

    # Start tick counter for calculating FPS (Frame per Second)
    tickmark = cv2.getTickCount()

    # Convert initial image in gray (better result)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Search the coordinate of the face in image
    faces = detectorModel.detectMultiScale(gray_frame, scaleFactor = 1.2, minNeighbors = 7, minSize = (70, 70))

    # Draw a red rectangle on recognized face
    for x, y, w, h in faces:
        gray_frame_resized = cv2.resize(gray_frame[y:y + h, x:x + w], (70, 70))
        user_id, confidence_index = recognizer.predict(gray_frame_resized)

        # If confidence index prediction is less than 100
        if confidence_index < threshold_confidence_index:
             color = userColorGranted
             name = labels[user_id]

        else:
            color = userColorUnknown
            name = "Unknown"
            print("Nb intrusion: {}".format(str(nb_intrusion)))
            nb_intrusion_total += 1
            intrusion = True

        label = name + " " + '{:5.2f}'.format(confidence_index)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 1, userColorInfo, 1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    # Calculate number of Frame Per Second (FPS), 1 frame = 1 image on screen
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - tickmark)
    
    # COMMANDS HUD
    cv2.rectangle(frame, (0, 0), (frameWidth, 30), (100, 100, 100), cv2.FILLED)
    cv2.putText(frame, "[ESC] Quit", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "Face(s):", (110, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)
    cv2.putText(frame, "{}".format(str(len(faces))), (180, 22), cv2.FONT_HERSHEY_PLAIN, 1.25, (0, 0, 255), 0)
    cv2.putText(frame, "FPS:", (frameWidth - 110, 20), cv2.FONT_HERSHEY_PLAIN, 1, userColorInfo, 1)
    cv2.putText(frame, "{:05.2f}".format(fps), (frameWidth - 70, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1)
    # cv2.putText(frame, "Unknown: {}".format(str(nb_intrusion)), (300, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 0)

    if intrusion:
        cv2.putText(frame, "INTRUSION DETECTED!", (250, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
        nb_intrusion += 1
    
    if nb_intrusion > 9:
        cv2.putText(frame, "SEND ALERT!", (150, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
        nb_intrusion = 0
        # TODO => Envoyer un sms & mail.

    cv2.imshow(" Identifying...", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        print("Nb total intrusion (frames): {}".format(str(nb_intrusion_total)))
        print("\n[X] - Stop identifiyng!", "\n")
        break

camera.release()
cv2.destroyAllWindows()
