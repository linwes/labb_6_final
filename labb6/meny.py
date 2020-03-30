import os
import sys
import cv2
import numpy as np
import time
from PIL import Image
import face


def meny ():

    print("1. Face detect and data gathering")
    print("2. Face training")
    print("3. ansikts igenkänning")
    print("4. avsluta")
    svar = input("Välj ett alternativ: ")

    while not svar == "":
        if svar == "1":
            face.spara()
            tillbaka()
            break
        elif svar == "2":
            face.träna()
            tillbaka()
            break
        elif svar == "3":
            face.igenkänning()
            tillbaka()
            break
        elif svar == "4": 
            sys.exit(0)            
            
def tillbaka():
    svar = input("vill du gå tillbacka till menyn skriv ja, vill du avsluta programet klicka vallfri knapp ")
    if svar == "Ja" or svar == "j" or svar == "J" or svar =="ja":
        meny()
    else:
        sys.exit()        
        
if __name__ == "__main__":
    meny()
    
    