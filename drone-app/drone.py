#!/usr/bin/python3
"""
@brief      This is program for automate Tello Drone.
@author     Yiğit GÜMÜŞ
@date       01-07-2023 (my DOB)
"""
# import necessary libs
import threading
from functools import partial
import sys
import time

# import my lib
from tellocommand import TelloCommand
from tellosensor import TelloState
from tellostream import TelloStream

# import ai things
# salih buraya ekle ai'yı

class TelloAutomation(object):
    def __init__(self):
        print("===GASERVER's Tello Drone Automation===")
        self.drone = TelloCommand()
        self.sensors = TelloState()
        self.video_frame = TelloStream()
        
        "@brief: open commander mode and init reading/response threads!"
        self.drone.send("command")
        self.initialize_receiver_threads()

    def emergency(self):
        "@brief: stops motors"
        self.drone.send("emergency")

    def terminate(self):
        "@brief: landing drone and exit programme."
        self.drone.send('land')
        print("Landing and Exiting...")
        self.droneThread.join()
        self.sensorThread.join()
        self.videoThread.join()
        time.sleep(10)
        sys.exit(0)

    def initialize_receiver_threads(self):
        '''
        @brief  Declare variables to parallel of my lib's classes
                and multithread them.
        '''
        self.droneThread = threading.Thread(target=self.drone.recv)
        self.droneThread.start()

        self.sensorThread = threading.Thread(target=self.sensors.recv)
        self.sensorThread.start()

        self.videoThread = threading.Thread(target=self.video_frame.recv)
        self.videoThread.start()

    def make_movement_decision(self) -> tuple[int, int, int, int]:
        '''
        @brief: make decision to move which direction in 3D space.
        '''
        while (True):
            self.posX = 0
            self.posY = 0
            self.posZ = 0
            self.speed = 50
            
            # do some stuff with image processing .d

            if self.speed < 10 or self.speed > 100:
                self.drone.send("land")
                print(f"Speed must be 10 <= x <= 100\nVelocity: {self.speed}cm/s")
            
            if self.posX < 0 and abs(self.posX) > 20 and abs(self.posX) < 500:
                self.drone.send(f"left {abs(self.posX)}")
            elif self.posX > 20 and self.posX < 500:
                self.drone.send(f"right {self.posX}")
            else:
                print(f"Your x-axis decision is wrong (must be in [20,500]! X: {self.posX}")
                self.terminate()
            
            if self.posY < 0 and abs(self.posY) > 20 and abs(self.posY) < 500:
                self.drone.send(f"down {abs(self.posY)}")
            elif self.posY > 20 and self.posY < 500:
                self.drone.send(f"up {self.posY}")
            else:
                print(f"Your y-axis decision is wrong (must be in [20,500]! Y: {self.posY}")
                self.terminate()

            if self.posZ < 0 and abs(self.posZ) > 20 and abs(self.posZ) < 500:
                self.drone.send(f"back {abs(self.posZ)}")
            elif self.posX > 20 and self.posX < 500:
                self.drone.send(f"forward {self.posZ}")
            else:
                print(f"Your z-axis decision is wrong (must be in [20,500]! Z: {self.posZ}")
                self.terminate()
        
    def recv(self):
        "@brief: receive data from drone's sensors."
        for key, value in self.sensors.state.items():
            print(f"{key}: {value}")

# @brief: for not defined error by KeyboardInterrupt block.
automation = ""
try:
    if __name__ == "__main__":
        automation = TelloAutomation()
except KeyboardInterrupt:
    automation.terminate()