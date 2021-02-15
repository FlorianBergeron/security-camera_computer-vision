import cv2
import pickle
import numpy as np
import os
from datetime import date, timedelta, datetime

from src.variables.config import *
from src.variables.global_variables import *

from src.notification.MailNotification import *
from src.notification.SmsNotification import *


def realTimeRecognizer():
    create_directory(path_intrusion_picture)
    classMail = MailNotification(sender_address, sender_pass, receiver_address)
    classSms = None

    current_path = os.getcwd() 

    if account_sid is not None and auth_token is not None and phone_auth is not None:
        classSms = SmsNotification(account_sid, auth_token, phone_auth)
    
    if not os.path.exists(path_intrusion_picture):
        os.makedirs(path_intrusion_picture)
    
    intrusion_picture_list = os.listdir(path_intrusion_picture) # dir is your directory path
    
    # variables 
    intrusion = False
    sendAlert = False
    alreadySend = False
    nb_intrusion = 0
    nb_intrusion_total = 0

    number_files = 0

    dtNow = datetime.now() - timedelta(days=1)

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
                # print("Nb intrusion: {}".format(str(nb_intrusion)))
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

        if intrusion:
            cv2.putText(frame, "INTRUSION DETECTED!", (250, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            nb_intrusion += 1
        
        if nb_intrusion > 9:
            cv2.putText(frame, "SEND ALERT!", (150, 250), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            nb_intrusion = 0
            sendAlert = True

        if sendAlert and (datetime.now()-dtNow).total_seconds() > notification_timer_seconds:
            intrusion_file_count = len(intrusion_picture_list)
            filename_attachement = "intrusion_" + str(intrusion_file_count + 1) + ".png"
            cv2.imwrite(os.path.join(path_intrusion_picture, filename_attachement), frame)
            classMail.send_mail(subject, body, current_path + "\intrusion\\" + filename_attachement)
            dtNow = datetime.now()
            alreadySend = True  
            sendAlert = False 
            if  classSms is not None :
                classSms.sendSms(body, user_phone)
            print("SENT!")
            
            number_files += 1

        cv2.imshow(" Identifying...", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            print("Nb total intrusion (frames): {}".format(str(nb_intrusion_total)))
            print("\n[X] - Stop identifiyng!", "\n")
            break

    camera.release()
    cv2.destroyAllWindows()

def create_directory(path):
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print("ok")