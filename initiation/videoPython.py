import picamera
from time import sleep

with picamera.PiCamera() as camera:
	camera.start_recording("/home/pi/Bureau/esgi-fyc/video.h264")
	sleep(4)
	camera.stop_recording()
	