
from sconf import Settings
import os,sys
import cv2 as cv
from utils import Detector
import random
import  numpy as np
from  threading import Thread
from  time import process_time, time
import logging
from sconf import Settings
import pyautogui as auto


logging.basicConfig(filename="run_log.txt", level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class Calculate:

    def __init__(self):
        self.templates=[]
        self.templates_bite=[]
        self.adjust_pixel_color = 0
        self.changed_pixel_value = 0 
        self.pixel_offset = 0
        self.bober_pixel_values = []
        # self.values_return=()
        # self.found_match = None
        # self.max_loc = None
        # self.higiest_match = None

    def worker_max_val(self,n):
        ts = time()
        obj = Calculate()
        obj.populate()
        obj.calculate_max_val(n)
           
        logging.info('calculate_max_val took  %s seconds', time() - ts)
        

    def populate(self):
        ts=time()
        settings  = Settings()
        dir= settings.read("captures", "template_dir")
       
        for  x in os.listdir(dir):
            if  x.endswith("png"):
                self.templates.append(cv.cvtColor(cv.imread(f"{dir}/{x}"),cv.COLOR_BGR2GRAY))
                
        
        dick = {}
        k= 0 
        files_in_dir = len(os.listdir(dir))
        split_in_chunks = round(files_in_dir/5)
        logging.info('list polulate  took  %s seconds', time() - ts)
        return[self.templates[x:x+split_in_chunks] 
        for x in range(0, len(self.templates), split_in_chunks)]
          
       
           
        #return self.templates
    
    def populate_bite(self):
        ts=time()
        settings  = Settings()
        dir= str(settings.read("captures", "template_bite_dir"))
        image_type = str(settings.read("captures", "template_bite_type"))
        print ("dir from bite ",dir)
        print(image_type)
        for  x in os.listdir(dir):
            if  x.endswith("jpg"):
                self.templates_bite.append(cv.cvtColor(cv.imread(f"{dir}/{x}"),cv.COLOR_BGR2GRAY))
               
        files_in_dir = len(os.listdir(dir))
        split_in_chunks = round(files_in_dir/5)
        logging.info('list bite polulate  took  %s seconds', time() - ts)
        return[self.templates_bite[x:x+split_in_chunks] 
        for x in range(0, len(self.templates_bite), split_in_chunks)]
          
    
    
    
    
    
    
    def calculate_max_val(self,template):
        ts = time()
        ppid = os.getpid()
        found_match = True
        #print(' Max Function process id:', os.getpid())
        find= Detector()
        res = random.choice(template)
        src = find.capture(find.area)       
        res = find.apply_template(src,res)
        
        _, max_val, _, max_loc=cv.minMaxLoc(res)
        higiest_match = max_val

        for dtemplate in template:
             res = find.apply_template(src,dtemplate)
             _, max_val, _, max_loc = cv.minMaxLoc(res)
             
             
             if max_val > higiest_match:
                 higiest_match = max_val
                 max_loc = max_loc
                 # print (f"max  value is : {max_val} and the max location  is: {max_loc}, ")
        
    
        if higiest_match < 0.80:
            #print(f"Match not found , the  final Value was {higiest_match}")
            found_match = False
        
        #w, h = final_template.shape[::-1]
        #print (final_template)
        #print(f"The w :{w}, the h is: {h}")
        #print(f"The final Value is {higiest_match} found match {found_match}")
        logging.info('Pid %s calculating max value  took  %s seconds', os.getpid() ,time() - ts)
        
        return [ found_match,max_loc,higiest_match,os.getpid()]

    def bitex(self):
        stime = time()
        white_px = 0
        height = 100
        width = 100
        x, y = auto.position()
        top = int(y - height / 2)
        left = int(x - width / 2)
        area = {"top": top, "left": left, "width": width, "height": height}
        bite = False
        utils = Detector()
        settings = Settings()
        pixel_color = int(settings.read("pixel", "pixel_color"))
        utils.area = area
        img = utils.capture(area)
        #changed_pixel_value = 0
        #adjust_pixel_color = 0
        #black_px = cv.countNonZero(img)
        #print(black_px)
        if self.adjust_pixel_color > 0:
            pixel_color = pixel_color - self.changed_pixel_value
            white_px_init = np.sum(img < pixel_color)
            logging.info(
                'changing the color values to:    %s ', pixel_color)
        else:
            white_px_init = np.sum(img < pixel_color)

        while not bite:
            if time() - stime < 21:
                    img = utils.capture(area)
                    white_px = np.sum(img < pixel_color)
                    self.bober_pixel_values.append(white_px)
                    #black_px = cv.countNonZero(img)
                    #print(white_px )
                    #print(f"white Px current:{white_px}  init Values:{white_px_init}")
                    if white_px < white_px_init - self.pixel_offset:
                        #print(f"white current:{white_px}  init{white_px_init}")
                        
                        bite == True
                        if time() - stime < 1:
                            print("To fast")
                            self.adjust_bober_pixel_offset()
                        
                        #self.adjust_bober_pixel_offset()
                        return True


            else:
                if np.average(self.bober_pixel_values) == white_px_init:
                    self.changed_pixel_value +=2
                    
                    if self.adjust_pixel_color > 10:
                        logging.error(
                            'Exit .I cant detect Bite, changing the pixel color values did nothing   %s Values', self.changed_pixel_value)
                        os._exit(1)

                logging.warning(
                     "Failed to detect bite ajusting parameters")
                self.adjust_bober_pixel_offset()
                break
      
                

    def adjust_bober_pixel_offset(self):
        min_val = np.min(self.bober_pixel_values)
        max_val = np.max(self.bober_pixel_values)
        print(f"min Val {min_val}, max val {max_val}")
        self.pixel_offset = (max_val - min_val) * 0.75 
        
        print(len(self.bober_pixel_values))
        logging.info(
            'changing Pixel Offset  values to:    %s ', self.pixel_offset)
    def clear_bober_values(self):
        self.bober_pixel_values = []

    def average_bober_pixel_offset(self):
       
        logging.info(
            'Median Pixel Offset  is:    %s ',  np.median(self.bober_pixel_values))


if __name__ == "__main__":
    
   pass
