import sys
from src.photoBooth_v2 import *
from src.trainLBPHFaceRecognizer import *
from src.realTimeFaceRecognizer import *


def userActionChoice():
    isValidChoice = False
    choice = None

    while isValidChoice == False:
        sys.stdout.write("\nWhat do you want to do? \n")
        sys.stdout.write("p : Take photos from new user. \n")
        sys.stdout.write("t : Train model. \n")
        sys.stdout.write("m : Monitor your home. \n")
        sys.stdout.write(" > ")
        choice = input()
        
        if choice == "p" or choice == "t" or choice == "m":
              isValidChoice = True
        else:
            sys.stdout.write("\nOption inexistante\n")

    return choice


def action(choice):
    if choice == "p":
        photoBooth()
    if choice == "t":
        trainModel()
    if choice == "m":
        realTimeRecognizer()
