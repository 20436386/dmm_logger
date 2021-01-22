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
import argparse

parser = argparse.ArgumentParser(description = "This program reads data from the GWINSTEK GDM-8261A multimeter over a RS232 connection. The data read is displayed as a graph and the raw data is stored in a .csv file - the graph is also stored as a .png file. Ensure that the multimater is connected and turned on(with the correct configuration setup on the actual device) before this program is run.")
parser.add_argument("File_name", help = "The name of the csv file where measured data will be stored", type = str)
parser.add_argument("Signal", type = str, help = "The signal being measured i.e. Voltage")
parser.add_argument("Mode", type = str, help = "This can either be the value \"AC\" or \"DC\"")
parser.add_argument("Sample_duration", type = float, help = "The duration over which the sampling takes place")
parser.add_argument("Time_step", type = float, help = "The sampling period in seconds i.e. time between succesive samples")
args = parser.parse_args()

sampling_period = args.Time_step - 0.003525398 #executioon of program adds samplig error
#copy_num = 0
current_time = 0
#graphing variables:
x_axis = []
y_axis = []

def graph():
    plt.plot(x_axis, y_axis)
    plt.title(args.Signal + " vs " + "Time")
    plt.xlabel('Time')
    plt.ylabel(args.Signal +'(' + args.Mode + ')')
    fig = plt.gcf()
    fig.savefig(args.File_name + ".png")
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

    while(current_time <= args.Sample_duration):
        #print(f"Value: {report(dmm)}")
        #print(f"current_time = ", current_time)
        sample = report(dmm)
        line = [current_time, sample]
        x_axis.append(current_time)
        y_axis.append(sample)

        with open(args.File_name + ".csv", "a") as log_file:
            log_writer = csv.writer(log_file,dialect='excel' )#,quoting= csv.QUOTE_NONNUMERIC)
            log_writer.writerow(line)

        current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time
        time.sleep(sampling_period)
    
    graph()

if __name__ == "__main__":
    main()

