import os
import sys
import cv2
import numpy as np
import time
from PIL import Image
import face


def meny ():
    print("Välkommen!")
    print("1. Face detect and data gathering")
    print("2. Face training")
    print("3. Face recognition")
    print("5. Quit")
    svar = input("Välj ett alternativ: ")

    while not svar == "":
        if svar == "1":
            face.data_collect()
            tillbaka()
            break
        elif svar == "2":
            face.trainer()
            tillbaka()
            break
        elif svar == "3": 
            face.face_detect()
            tillbaka()
            break 
        elif svar == "4":
            face.face_reco()
            tillbaka()
            break
        elif svar == "5": 
            sys.exit(0)            
            
def tillbaka():
    svar = input("Vill du gå tillbaka till menyn? Y/N: ")
    if svar == "Yes" or svar == "y" or svar == "Y" or svar =="yes":
        meny()
    else:
        sys.exit()        
        
if __name__ == "__main__":
    meny()
    