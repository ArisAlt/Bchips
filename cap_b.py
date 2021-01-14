import pyautogui as pag
import time, sys, os
import cv2 as cv
import numpy as np
from loguru import logger
from mss import  mss
from  mss import tools
from pynput import keyboard
from pynput.keyboard import Listener
#import tty
from datetime import datetime

width = 50
height = 50
directory = 'images'
count=0



def on_press(key):

    ##72 is h
    if key == keyboard.Key.end:
        print("end is pressed")
        return False
    ##123 is esc 
    if key == keyboard.Key.f12:
        print("f12 is pressed")    
        capture()

def capture():
        
    with mss() as sct:
        global count
        x, y = pag.position() 
        top = int(y - height / 2) 
        left = int(x - width / 2)       
        area = {
        "top": top,
        "left": left,
        "width": int(width),
        "height": int(height)
        }   
        print (f"x is {x} , y is {y}")
        print({area["top"]})
        
        
        im = np.array(sct.grab(area))
        cv.imwrite(directory + '/template_ba1' + f"{count}" + '.png', im)
        cv.imshow('preview', im)
        cv.waitKey(25)
        cv.destroyAllWindows()
        print(ord("h"))    
        count += 1
        logger.info(f"({x}, {y})")

     

def start():
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join()

if __name__ == "__main__":
    start()
  
      
        

