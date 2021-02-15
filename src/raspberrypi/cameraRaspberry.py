import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1280, 720))

# Allow the camera to warmup
time.sleep(0.1)

# Main loop app
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Read each frame of the video (frame per frame) in numpy array
	image = frame.array

	# Display this image on the screen
	cv2.imshow(" Capturing - Press ESC to quit", image)

	# Wait until key button is pressed
	key = cv2.waitKey(1) & 0xFF

	# Clear stream in preparation for the next frame
	rawCapture.truncate(0)

	# Press ESCAPE to stop app (ASCII code decimal = 27)
	if key == 27:
		break
