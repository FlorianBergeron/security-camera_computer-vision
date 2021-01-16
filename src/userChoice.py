import sys
from src.photoBooth_v2 import *
from src.trainLBPHFaceRecognizer import *
from src.realTimeFaceRecognizer import *

def userActionChoice():
    isValidChoice = False
    choice = None

    while isValidChoice == False:
        sys.stdout.write("\nQue voulez vous faire ? \n")
        sys.stdout.write("-p : Prendre des photo d'un nouvel utilisateur \n")
        sys.stdout.write("-t : Entrainer le modèle \n")
        sys.stdout.write("-s : Surveiller ma maison \n")
        sys.stdout.write("A vous de choisir : ")
        choice = input()
        
        if choice == "p" or choice == "t" or choice == "s":
              isValidChoice = True
        else:
            sys.stdout.write("\nOption inexistante\n")

    return choice

def action(choice):
    if choice == "p":
        photoBooth()
    if choice == "t":
        trainModel()
    if choice == "s":
        realTimeRecognizer()

    