
import os,sys
from utils import Detector
import numpy as np
import cv2 as cv
from mss import exception as MSSException
from show import Show
from sconf import Settings
import mss
from pynput import keyboard
from pynput.keyboard import Listener
from threading import Thread
from multiprocessing import Pool

kill = False

def on_press(key):
    global kill 
    ##72 is h
    if key == keyboard.Key.end:
        print("end is pressed")
        kill = True
        ## to kill lisener return False 
        ## to  stop the proc use os_exit(proc)
        os._exit(os.EX_OK)
    ##123 is esc 
    if key == keyboard.Key.f12:
        print("f12 is pressed")    
        high_val()
    
    
        


def  high_val():
     
    monitor_size = Detector()
    det = Detector()
    settings = Settings()
    detection_method = int(settings.read(
        section="detectors", parameter="method"))
    template_image = settings.read(
        section="captures", parameter="template_image")
    global kill     
    while not kill == True:    
        with mss.mss() as sct:
                # The screen part to capture
                #monitor = {"top": 268, "left": 2300, "width": 1400, "height": 600}
                #output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
                # Grab the data
                try:
                    src = cv.cvtColor(np.array(sct.grab(monitor_size.area)),
                                    cv.COLOR_BGRA2GRAY)
                except (MSSException.ScreenShotError):
                    print("Sc_error")
                #send photo to auto_canny
                #src = det.auto_canny(src)
                top_monitor = monitor_size.area["top"]
                left_monitor = monitor_size.area["left"]
                

        image = cv.imread(template_image, 0)
        w, h = image.shape[::-1]
        #image = det.auto_canny(image)
        # Apply template Matching
        res = cv.matchTemplate(src, image, detection_method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # added to find bottom_right
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        # find object mid point and get x,y
        move_at_x = max_loc[0] + h / 2 + left_monitor
        move_at_y = max_loc[1] + w / 2 + top_monitor
        #add some test for debug 
        cv.rectangle(src,top_left, bottom_right, 255, 2)
        cv.imshow('preview', src)
        cv.waitKey(500)
        cv.destroyAllWindows() 
        with Listener(on_press=on_press):
            break
        


def start():
   
    
    listener = Listener(on_press=on_press)
    listener.start()
    listener.join() 

    
#     # #listener.start()
#     # #Thread(target=high_val).start()
#     # listener = Listener(on_press=on_press)
#     # listener.start()
#     # listener.join()
     
def test2():
  list_1=[1,3,4,5,6]
  split_in_chunks = 2 
  list_1[1:2+split_in_chunks]
  print(list_1)


def test3():
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

if __name__ == "__main__":
    print(test3())





  