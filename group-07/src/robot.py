#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time
from typing import List


class Robot:
    """
    -- TEMPLATE --
    This class provides logic for moving the sensor and scrolling the bar code cards
    """

    def sensor_step(self):
        """
        Moves the sensor one step to read the next bar code value
        """
        # implementation
        m = ev3.LargeMotor("outA")
        time.sleep(1.8)
        m.reset()
        m.polarity = "inversed"
        m.stop_action = "brake"
        m.position_sp = 150#50
        m.speed_sp = 95#18
        m.command = "run-to-rel-pos"
        time.sleep(0.52)
        m.stop()

    def sensor_reset(self):
        """
        Resets the sensor position
        """
        # implementation
        m = ev3.LargeMotor("outA")
        m.reset()
        #m.polarity = "inversed"
        m.stop_action = "brake"
        m.position_sp = 1650
        m.speed_sp = 1045
        m.command = "run-to-rel-pos"
        time.sleep(0.52)
        m.stop() 
        m.stop_action = "brake"
        m.position_sp = 490
        m.speed_sp = 310
        m.command = "run-to-rel-pos"
        time.sleep(0.52)
        m.stop()

    def scroll_step(self):
        """
        Moves the bar code card to the next line.
        """
        # implementation
        page_motor = ev3.LargeMotor("outD")
        page_motor.reset()
        page_motor.polarity = "inversed"
        page_motor.stop_action = "brake"
        page_motor.position_sp = 90 #150
        page_motor.speed_sp = 40 #189
        page_motor.command = "run-to-rel-pos"
        time.sleep(10)
        page_motor.stop()

    def read_value(self) -> int:
        """
        Reads a single value, converts it and returns the binary expression
        :return: int
        """
        # implementation
        cs = ev3.ColorSensor()
        cs.mode = 'RGB-RAW'
        r = []
        b = []
        for i in range(10):
            time.sleep(0.02)
            output = cs.bin_data("hhh")
            r.append(output[0])
            b.append(output[2])
        tuple(r); tuple(b)
        mode_r = self.calc_freq(r)
        mode_b = self.calc_freq(b)
        output = self.output_col(mode_r,mode_b)
        return output

    def calc_freq(self, Tuple):
        count1 = 0; count2 = 0
        for i in Tuple:
          if i < 200:
            count1 = count1 + 1
          else:
            count2 = count2 + 1
            
        if count1 > count2:
          output = 150
        else:
          output = 250
        #print(output)
        return output   

    def output_col(self,r,b):
        if (r < 200 and b < 200):
            return 1
        else: 
            return 0
        
    def row_scan(self) -> List:
        time.sleep(1.8)
        res = []
        res.append(self.read_value())
        #res = self.read_value()
        #print(res, end=" ")
        for i in range(11):
            if (i != 11):
                self.sensor_step()
                self.read_value() 
                res.append(self.read_value())
                #res = self.read_value()
                #print(res, end=" ")  
        time.sleep(2)
        self.sensor_reset()
        return res
        #print()
        
        
def main():
    r = Robot()
    for i in range(10):
        r.row_scan()
        r.scroll_step()
    
if __name__=="__main__":
    main()