import os
import cv2

# Directory paths
WORKSPACE = "../"
DATA_DIR = WORKSPACE + "dataset/"

# Variables
nb_img = 0
frameWidth = 640
frameHeight = 480

name = str(input("\n[?] - What is your dataset's name?\n > "))

try:
    os.mkdir(DATA_DIR)
except:
    pass

try:
    os.mkdir(DATA_DIR + name)
except:
    pass

print("\n[!] - Start capturing...")

camera = cv2.VideoCapture(0)

camera.set(3, frameWidth)
camera.set(4, frameHeight)

# cv2.namedWindow(" Take photo => spacebar", cv2.WINDOW_NORMAL)
# cv2.resizeWindow(" Take photo => spacebar", 500, 300)

while True:
    _, frame = camera.read()
    
    if not _:
        print("[X] - Failed to take photo")
        break
    # TODO: Display total number of photos taken (but appears on screenshot...)
    # cv2.putText(frame, 
    #             "Photos: {}".format(nb_img), (5, 30), 
    #             cv2.FONT_HERSHEY_PLAIN, 2, 
    #             (255, 255, 0), 2)
    cv2.imshow(" Capturing {} => SPACEBAR".format(str(name)), frame)

    # Wait until key button is pressed
    key = cv2.waitKey(1) & 0xFF
    
    # Press ESCAPE to stop app (ASCII code decimal = 27)
    if key == 27:
        print("[!] - Photos taken: {}".format(nb_img))
        print("\n[X] - Stop capturing!", "\n")
        break

    # Press SPACEBAR to take a photo (ASCII code decimal = 32)
    if key == 32:
        filename = DATA_DIR + name + "/image_{}.jpg".format(nb_img)
        cv2.imwrite(filename, frame)
        print(" > [+] {} has been saved!".format(filename))
        nb_img += 1

camera.release()
cv2.destroyAllWindows()
