
import os, sys
import random
import numpy as np
from threading import Thread
import threading
import time
import logging
from utils import Detector
from server_update import Calculate
from multiprocessing import Process, Queue, Pool
#from pool_processes import max_join_pool_values
import pyautogui as auto
import random
from pynput import keyboard
from pynput.keyboard import Listener
from screen_setup import screen_setup
import ctypes
import platform
#from tkinter import *

logging.basicConfig(filename = "log.log",level=logging.INFO, format='%(asctime)s - %(message)s')

logger = logging.getLogger(__name__)

wtf = Calculate()
utils = Detector()
token = 0
torun =  True
def cast():
        auto.keyDown('f8')
        auto.keyUp('f8')
        time.sleep(0.5)
    
def recast(found):
    random_recasts = random.uniform(7,11)
    max_trys=0
    while not found:
        max_trys += 1
        time.sleep(random.uniform(2,5))
        cast()
        found, max_loc, max_value = max_join_pool_values()
        if max_trys > random_recasts:
            logging.error(' i cant find the Bobber ,Stoped  max Trys  %s ', max_trys)
            return False ,sys.exit("oops Max trys has been reached")

    return max_loc




def on_press(key):
    global torun
    has_run = False  
    if key == keyboard.Key.end:
        print ("Closing... ")
        torun = False
        return torun , sys.exit(0)
    ##123 is esc 
    if key == keyboard.Key.f12:
        global token 
        token += 1 
        if token == 1:
            utils.focus_on_window()
            print("Running..")
            start_run_thread()

    if key == keyboard.Key.f5:
        utils.focus_on_window()
        screen_setup().run_setup()
       
       #utils.focus_on_window()
    if key == keyboard.Key.pause:
        
        if has_run:
            print("Unpause")
            utils.focus_on_window()
            has_run = False 
            
        elif not has_run:
            print("Pause ... Press the Pause key again to continue")
            has_run = True
           







def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def run():
    global torun
    info("Process Info")
    #print(threading.enumerate())

    #with Listener(on_press=on_press):
    while torun:
       
            time.sleep(0.5)
            
            cast()
            print("cast")
            found, max_loc, _ = max_join_pool_values()   
            if not found:
                max_loc = recast(found)
                print("recast")
            x,y = utils.move_to(max_loc)
            
            if wtf.bitex():
                time.sleep(random.uniform(1, 2))
                auto.click()
                time.sleep(random.uniform(1, 3))
                wtf.adjust_pixel_color -= 1
                wtf.average_bober_pixel_offset()
                wtf.clear_bober_values()
            else:
                wtf.adjust_pixel_color += 1
                wtf.average_bober_pixel_offset()
                wtf.clear_bober_values()
        ## add click 
    return False

def start_keyboard_l():
    
    listener = Listener(name = "keyBoard_Listener", on_press=on_press)
    listener.start()
    listener.join()
def start_run_thread():
    runThread = Thread(name = "run_thread", target=run, daemon=True)
    runThread.start()
def init_run():
    PROCESS_PER_MONITOR_DPI_AWARE = 2
    ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
    
   
    #lisenerThread = Thread(target=start_l)
   
    time.sleep(random.uniform(1, 5))
    try:
        utils.focus_on_window()
       
       
    except:
       
        sys.exit(logging.info(
            'WoW is not ruuning ... '))

    finally:
        pass
       
        
    
   
    print("F12 to start")
    #mainThread.join()  

        


def max_pool_processes():
    wtf = Calculate()
    list_templates = []

    list_templates = wtf.populate()
    with Pool(processes=5) as pool:
        try:
            p1 = pool.map(wtf.calculate_max_val, list_templates)
        except SystemExit:
            print("Shutdown")

        finally:
            pool.close()
            pool.join()
            pool.terminate()

    return p1


def max_join_pool_values():
    found = False
    max_loc = (0, 0)
    max_val = -1
    max = 0
    for x in max_pool_processes():
        for y in x:
            value_in_tuple = x[2]
        if x[0] is True and value_in_tuple > max:
            max = x[2]
            found = x[0]
            max_loc = x[1]
            max_val = x[2]
    logging.info('Found  is: %s max location is:  %s and max value is %s',
                 found, max_loc, max_val)
    return found, max_loc, max_val


def main():
    init_run()
    start_keyboard_l()


if __name__ == "__main__": 
   main()
