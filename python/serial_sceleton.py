#!/usr/bin/python3
import sys
import serial
import time
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse

#global variables:
dmm = None
dmm = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=1)
current_time = 0
#graphing variables:
x_axis = []
y_axis = []

#helper functions:
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

def shift(array, length):
    for i in range(int(length-1)):
        array[i] = array[i+1]
    array.pop(int(length-1))

def animate(i, *args):
    current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - args[1]
    sample = report(dmm)
    x_axis.append(current_time)
    print(current_time) #print every 0.02816448 (0.1)  0.025755751
    y_axis.append(sample)
    length = args[2]/args[3]
    #print("length of array = " + str(len(y_axis)))
    if len(y_axis) > length:
        #print("condition met, len(x_axis) = " + str(len(y_axis)))
        shift(x_axis, length)
        shift(y_axis, length)
    args[0].clear()
    args[0].plot(x_axis,y_axis)

def graph(args):
    plt.plot(x_axis, y_axis)
    plt.title(args.Signal + " vs " + "Time")
    plt.xlabel('Time')
    plt.ylabel(args.Signal +'(' + args.Mode + ')')
    fig = plt.gcf()
    fig.savefig(args.File_name + ".png")
    plt.show()

#sub-command functions:
def track(args):
    #define figure:
    fig = plt.figure()
    graph1 = fig.add_subplot(1,1,1)
    start_time = time.clock_gettime(time.CLOCK_BOOTTIME)
    animate_args = (graph1, start_time, args.Domain, args.Time_step)
    #print("Time_step = " + str(args.Time_step * 1000))
    time_step = args.Time_step - 0.026760728 #sampling error added by execution time of program
    #animate:
    ani = animation.FuncAnimation(fig, animate, fargs = animate_args, interval = (time_step * 1000))
    plt.show()

def save(args):
    sampling_period = args.Time_step - 0.003525398 #executioon of program adds samplig error
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
            log_writer = csv.writer(log_file, dialect='excel')#,quoting= csv.QUOTE_NONNUMERIC)
            log_writer.writerow(line)

        current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time
        time.sleep(sampling_period)
    
    graph(args)


#create the top-level parser
parser = argparse.ArgumentParser(description = "This program reads data from the GWINSTEK GDM-8261A multimeter over a RS232 connection. Ensure that the multimater is connected and turned on(with the correct configuration setup on the actual device) before this program is run.")
subparsers = parser.add_subparsers(help = "sub-command help")

#creating parser for "track command":
parser_track = subparsers.add_parser("track", help = "This command will display a graph that tracks the samples taken from the multimeter.")
parser_track.add_argument("Domain", type = int, help = "The domain of the graph to be displayed")
parser_track.add_argument("Time_step", type = float, help = "The sampling period in seconds i.e. time between succesive samples")
parser_track.set_defaults(func = track) #define the tracking function now

#creating parer for "save" command:
parser_save = subparsers.add_parser("save", help = "This command will display the samples taken as a graph and store the raw data in a .csv file - the graph is also stored as a .png file.")
parser_save.add_argument("File_name", type = str, help = "The name of the csv file where measured data will be stored")
parser_save.add_argument("Signal", type = str, help = "The signal being measured i.e. Voltage")
parser_save.add_argument("Mode", type = str, help = "This can either be the value \"AC\" or \"DC\"")
parser_save.add_argument("Sample_duration", type = float, help = "The duration over which the sampling takes place")
parser_save.add_argument("Time_step", type = float, help = "The sampling period in seconds i.e. time between succesive samples")
parser_save.set_defaults(func = save)

#parse arguments and call whatever function was selected
args = parser.parse_args()
args.func(args)

# def main():

# if __name__ == "__main__":
#     main()

