import cv2

frameWidth = 640
frameHeight = 480

# Start video capture (0: built-in camera - 1, 2, ... are other camera connected by usb)
camera = cv2.VideoCapture(0)

# Setting openCV window dimension (640 width * 480 height in pixels)
camera.set(3, frameWidth)
camera.set(4, frameHeight)

# Main loop app
while True:
    # Read each frame of the video (frame per frame)
    _, frame = camera.read()

    # Display this image on the screen
    cv2.imshow(" Capturing", frame)

    # If "q" key is pressed, the app is shutdown
    key = cv2.waitKey(1) & 0xFF
    
    # Press ESCAPE to stop app (ASCII code decimal = 27)
    if key == 27:
        print("\n[X] - Stop capturing!", "\n")
        break

# Release camera to other software
camera.release()
cv2.destroyAllWindows()
