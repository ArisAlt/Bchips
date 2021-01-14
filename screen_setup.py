import json
from numpy.lib.function_base import append
import pyautogui as auto
from pynput import mouse
from pynput.mouse import Listener,Controller
import logging
import time
import json
import ctypes
logging.basicConfig(filename="log.log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
class screen_setup:
        def __init__(self):
            self.cords ={
                "top": 0,
                "left": 0,
                "width": 0,
                "height": 0

            }   
            self.cord_list =[]
            self.points = 1
        
        def on_click(self,x, y, button, pressed):
               
                if pressed:                   
                    print (f"position: {self.points} captured")
                    logging.info(
                        'Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
                    self.cord_list.append(x)
                    self.cord_list.append(y)
                    
                    self.points += 1
                    #print(self.cord_list)
                    if self.points == 2: 
                        print("Move the mouse to the Second location , bottom left corner") 
                   
                    if self.points == 3:
                       self.cords["top"] = self.cord_list[0]
                       self.cords["left"] = self.cord_list[1]
                       self.cords["width"] = self.cord_list[2] - self.cord_list[0]
                       self.cords["height"] = self.cord_list[3] - self.cord_list[1]
                       print(self.cords.items())
                       self.dump_cords()
                       logging.info(
                           'Screen setup finised press F12 to start the app')

                       return False,
               
                

        def run_setup(self):
            print ("Starting the area setup\n")
            time.sleep(1)
            print("Move the mouse to the Upper left corner and Left click")
            time.sleep(1)
            self.run_thread()
            # self.record_cords()

        def dump_cords(self):
            with open ("screen.json", mode= "w") as dump:
                json.dump(self.cords,dump)
           
               
                 
              
                
        def run_thread(self):
           listener =  Listener(on_click=self.on_click)
           listener.start() 


if __name__ == "__main__":
    screen_setup().run_setup()
    #time.sleep(10)
    
    #print(screen_setup().record_cords(0))    

