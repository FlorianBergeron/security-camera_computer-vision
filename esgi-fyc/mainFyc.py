import motionDetection3
import picamera
from datetime import datetime

picPath = "home/pi/Bureau/esgi-fyc/motionImages/"
motionState = False

def takePicture(currentTime, picPath):
	picName = currentTime.strftime("%Y.%m.%d-%H%M%S") + '.png'
	with picamera.PiCamera() as camera:
		camera.resolution = (1280, 720)
		camera.capture(picPath + picName)

	print("photo a été prise")

def getTime():
	currentTime = datetime.now()
	return currentTime


while True:
	motionState = motionDetection3.motionDetector()
	if motionState:
		currentTime = getTime()
		takePicture(currentTime, picPath)