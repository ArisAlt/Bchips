
from os import close
import os
import cv2 as cv
import logging
from server_update import Calculate
from  multiprocessing import Process, Queue,Pool
import server_update
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)



def worker(qe):
    pass

def poolcontext(*args, **kwargs):
    pool = Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def max_pool_processes():
    wtf = Calculate()
    list_templates = []
        
    list_templates = wtf.populate()
    with Pool(processes= 5) as pool:
        try:
            p1 = pool.map(wtf.calculate_max_val ,list_templates)
        except SystemExit:
            print("Shutdown")
                
        finally:
            pool.close()
            pool.join()
            pool.terminate()
    
    return  p1





def max_join_pool_values():
    found = False
    max_loc = (0,0)
    max_val = -1
    max =0 
    for x in max_pool_processes():
        for y in x:            
            value_in_tuple = x[2]
        if x[0] is True and value_in_tuple > max:
                max = x[2]
                found = x[0]
                max_loc = x[1] 
                max_val = x[2]
    logging.info('Found  is: %s max location is:  %s and max value is %s', found, max_loc,max_val)
    return found, max_loc, max_val        
            
# def max_join_pool_values_bite(list_template):
#     found = False
#     list_template = list_template
#     max_loc = (0,0)
#     max_val = -1
#     max =0 
#     for x in max_pool_processes_bite(list_template):
#         for y in x:            
#             value_in_tuple = x[2]
#         if x[0] is True and value_in_tuple > max:
#                 max = x[2]
#                 found = x[0]
#                 max_loc = x[1] 
#                 max_val = x[2]
#     logging.info('Found  is: %s max location is:  %s and max value is %s', found, max_loc,max_val)
#     return found, max_loc, max_val      
            


if __name__ == '__main__':
   pass
