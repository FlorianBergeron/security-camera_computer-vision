import picamera

#mettre en place la caméra de façon a ce qu'elle se ferme quand en aurons fini avec elle

print('entrain de prendre une photo')
with picamera.PiCamera() as camera:
	camera.resolution = (1280, 720)
	camera.capture("/home/pi/Bureau/esgi-fyc/imagePython.png")

print("photo a été prise")