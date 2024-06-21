#!/usr/bin/env python3

from hamming_code import HammingCode
from stack_machine import StackMachine
from robot import *
from typing import Tuple
#import ev3dev.ev3 as ev3
import time
import sys

err_count = 0
robot = Robot()
ham = HammingCode()
sm = StackMachine()

#def mov_sensor() -> Tuple[int, ...]:
#    barcode = []
#    time.sleep(3)
#    barcode.append(robot.read_value())
#    for i in range(11):
#        if (i != 11):
#            robot.sensor_step()
#            barcode.append(robot.read_value())
#        else:
#            time.sleep(5)
#            barcode.append(robot.read_value())   
#    robot.sensor_reset()
#    return tuple(barcode)

def mov_sensor() -> Tuple[int, ...]:
    barcode = robot.row_scan()
    return tuple(barcode)    

def multiple_pages(barcode: Tuple[int, ...]):
    if (barcode == (0,0,0,0,0,0,0,0,0,0,0,0) or barcode == (1,0,0,0,0,0,0,0,0,0,0,0)):
        flag = int(input("Press 1 for Inserting a new page or 0 to exit: "))
        if (flag == 1):
            print("Scanning new page")
            page_scan()
        elif (flag == 0):
            print("Exiting program!!") 
            sys.exit()   
         
#def page_scan():
#    code = mov_sensor()
#    barcode = (code[1:])
#    print(barcode)
#    multiple_pages(code)
#    dec_codeword = ham.decode(barcode)
#    print(dec_codeword)
#    if (dec_codeword==None):
#        global err_count
#        err_count = err_count + 1
#        if (err_count == 1):
#            print('uncorrectable code')
#            print('there may be an error in bit scan so i am initiating scanning process again')
#            page_scan()
#        elif (err_count >= 1):
#            print('uncorrectable code  and terminating program ')
#            sys.exit()
#    else:
#        #print('rescan worked well and errors got rectified ')
#        sm.do(dec_codeword)
#    robot.scroll_step()
#    page_scan()  
    
def page_scan():
    code = mov_sensor()
    barcode = (code[1:])
    print(barcode)
    multiple_pages(code)
    dec_codeword = ham.decode(barcode)
    print(dec_codeword)
    if (dec_codeword==None):
        print('uncorrectable code')
        print('there may be an error in bit scan so i am initiating scanning process again')
        time.sleep(10)
        page_rescan()
    else:
        sm.do(dec_codeword)
    robot.scroll_step()
    page_scan()
    
def page_rescan():
    code = mov_sensor()
    barcode = (code[1:])
    print(barcode)
    multiple_pages(code)
    dec_codeword = ham.decode(barcode)
    print(dec_codeword)
    if (dec_codeword==None):
        print('uncorrectable code')
        print('uncorrectable code and terminating program ')
        sys.exit()
    else:
        print('rescan worked well and errors got rectified ')
        sm.do(dec_codeword)
    robot.scroll_step()
    page_scan() 

def run():
    # the execution of all code shall be started from within this function
    print("Hello World!")
    page_scan()


if __name__ == '__main__':
    run()
