#!/usr/bin/python3
##################################################################################
#First commandline argument must be the name of the log file to be created.#######
#The second must be signal being measured i.e. Voltage or Current. The third###### 
# parameter must be either the value "AC" or "DC". the The fourth parameter must##
# be the sampling duration and the fith should be the sampling period(note that ##
# fastest sampling period appears to be 200ms)####################################
##################################################################################
import sys
import serial
import time
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

log_name = sys.argv[1]
signal = sys.argv[2]
mode = sys.argv[3]
test = sys.argv[6]
print(test)
sampling_duration = float(sys.argv[4]) 
sampling_period = float(sys.argv[5]) - 0.003525398 #executioon of program adds samplig error
#copy_num = 0
current_time = 0
#graphing variables:
x_axis = []
y_axis = []

def graph():
    plt.plot(x_axis, y_axis)
    plt.title(signal + " vs " + "Time")
    plt.xlabel('Time')
    plt.ylabel(signal +'(' + mode + ')')
    fig = plt.gcf()
    fig.savefig(log_name + ".png")
    plt.show()
    

def _readline(self):
    eol = b'\r'
    leneol = len(eol)
    line = bytearray()
    while True:
        char = self.read(1)
        #print("char read" + char.decode("utf-8") + "\n")
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
        #print(f"RX: {char}")
        reply_list = rx_line.split(',')
        str_value = reply_list[0].lower()
        #print(f"{str_value}")
        return float(str_value)

def main():
    dmm = None
    dmm = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=1)

    start_time = time.clock_gettime(time.CLOCK_BOOTTIME)
    current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time

    while(current_time <= sampling_duration):
        #print(f"Value: {report(dmm)}")
        #print(f"current_time = ", current_time)
        sample = report(dmm)
        line = [current_time, sample]
        x_axis.append(current_time)
        y_axis.append(sample)

        with open(log_name + ".csv", "a") as log_file:
            log_writer = csv.writer(log_file,dialect='excel' )#,quoting= csv.QUOTE_NONNUMERIC)
            log_writer.writerow(line)

        current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time
        time.sleep(sampling_period)
    
    graph()

if __name__ == "__main__":
    main()

