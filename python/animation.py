#!/usr/bin/python3
##################################################################################
#First commandline argument must be the name of the log file to be created.#######
#The second must be signal being measured i.e. Voltage or Current. The third###### 
# parameter must be either the value "AC" or "DC". the The fourth parameter must##
# be the sampling duration and the fith should be the sampling period(note that ##
# fastest sampling period appears to be 200ms)####################################
##################################################################################
#argparse checkout
import sys
import serial
import time
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

dmm = None
dmm = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=1)
current_time = 0
#graphing variables:
x_axis = []
y_axis = []

fig = plt.figure()
graph1 = fig.add_subplot(1,1,1)

def _readline(self):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        char = self.read(1)
        if char:
            line += char
            if line[-leneol:] == eol:
                break
        else:
            break
    return bytes(line)

def report(dmm):
    if dmm:
        dmm.write(b"read? buf\r")

        rx_line = _readline(dmm).decode("utf-8")
        reply_list = rx_line.split(',')
        str_value = reply_list[0].lower()
        return float(str_value)

def shift(array):
    for i in range(int((10/0.2)-1)):
        array[i] = array[i+1]
    array.pop(int((10/0.2)-1))

def animate(i):
    current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time
    sample = report(dmm)
    x_axis.append(current_time)
    y_axis.append(sample)
    if len(x_axis) > (10/0.2):
        shift(x_axis)
        shift(y_axis)
    graph1.clear()
    graph1.plot(x_axis,y_axis)

start_time = time.clock_gettime(time.CLOCK_BOOTTIME)

def main():
    ani = animation.FuncAnimation(fig, animate, interval = 200)
    plt.show()

if __name__ == "__main__":
    main()

