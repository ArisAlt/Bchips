from os import close
import numpy as np
from time import sleep
import cv2 as cv
import mss
from mss import exception as MSSException
import pyautogui as move
import random
from sconf import Settings
import pyautogui as auto
import time
import logging
import platform
import sys
import json
#import win32gui
from pywinauto import Application
#from server_update import 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Detector:
    
    def __init__(self):
        self.settings = Settings()
        #self.area = {"top": 268, "left": 2300, "width": 1400, "height": 600}
        #win Area
        
            
        self.area = self.settings.read_screen_area()

        #self.area = {"top": 100, "left": 200, "width": 1400, "height": 600}
    


    def normilize_cap(self):
        pass

    def auto_canny(self, image,sigma):
        # sigma = float(self.settings.read(
        #     section="detectors", parameter="sigma"))
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv.Canny(image, lower, upper)
        # return the edged image
        return edged

    def capture(self,area):
        area = self.area
        with mss.mss() as sct:
            # The screen part to capture
            
            # Grab the data
            try:
                src = cv.cvtColor(np.array(sct.grab(area)),cv.COLOR_BGRA2GRAY)
            except (MSSException.ScreenShotError):
                print("Sc_error")
       
        sct.close()
        #cv.destroyAllWindows()
        return src


    def capture_def(self):
        area = self.area
        with mss.mss() as sct:
            # The screen part to capture
            
            # Grab the data
            try:
                src = np.array(sct.grab(area))
            except (MSSException.ScreenShotError):
                print("Sc_error")
        
        sct.close()
        return src   

    def apply_template(self,source,template):
        
        res = cv.matchTemplate(source, template,5 )
        return res
    
    
    def move_to(self,max_loc):
        
        movetimer = random.uniform(0.5,0.7)
        top_monitor = self.area["top"]
        left_monitor = self.area["left"]
        
        
        # find object mid point and get x,y
        #move_at_x = max_loc[0] + 50 / 2 + left_monitor
        #move_at_y = max_loc[1] + 50 / 2 + top_monitor
        move_at_x = max_loc[0] + 50 / 2 + left_monitor
        move_at_y = max_loc[1] + 50 / 2 + top_monitor
        
        move.moveTo(move_at_x, move_at_y, duration=movetimer)
        return (move_at_x,move_at_y)

    def wint(self):
        if platform.system() == 'Windows':
            top, left, w, h = win32gui.GetWindowRect(
                win32gui.GetForegroundWindow())

    
        
    def focus_on_window(self):
        wow = Application().connect(path="Wow.exe", title="World of Warcraft")
        wow.WorldofWarcraft.set_focus()

    def read_screen_area(self):
        screen = "screen.json"
        area = {"top": 0, "left": 0, "width": 0, "height": 0}
        with open(screen, mode="r") as file:
            config = json.load(file)
            area["top"] = config["top"]
            area["left"] = config["left"]
            area["width"] = config["width"]
            area["height"] = config["height"]
        return area

def countdown(secs):
    while secs > 0:
        logger.info(str(secs) + "...")
        time.sleep(1)
        secs = secs - 1




    


if  __name__ == "__main__":
  pass
