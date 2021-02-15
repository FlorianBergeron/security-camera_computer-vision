import sys
from src.raspberrypi.recordUserDataset import *
from src.trainLBPHFaceRecognizer import *
from src.realTimeFaceRecognizer import *


def userActionChoiceRaspberry():
    isValidChoice = False
    choice = None

    while isValidChoice == False:
        print("\n***********************")
        print("Raspberry Pi - Version")
        print("***********************\n")
        
        sys.stdout.write("What do you want to do? \n")
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
        photoBooth_raspberry()
    if choice == "t":
        trainModel_raspberry()
    if choice == "m":
        realTimeRecognizer_raspberry()
