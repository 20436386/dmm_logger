#!/usr/bin/python3
#first commandline argument should be the sampling time and the second should be the sampling period
import sys
import serial
import time
import csv

sampling_time = float(sys.argv[1]) 
sampling_period = float(sys.argv[2])
dmm = None
dmm = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=1) #was 0.005
log_num = 0

#with open("log0" + str(log_num) + ".csv", "w+") as log_file:
#    log_writer = csv.writer(log_file, delimiter = ',')

current_time = 0

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
        #rx_line = dmm._readline().decode("utf-8")
        #print(f"RX: {char}")
        reply_list = rx_line.split(',')
        str_value = reply_list[0].lower()
        #print(f"{str_value}")
        return float(str_value)

start_time = time.clock_gettime(time.CLOCK_BOOTTIME)
current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time

while(current_time <= sampling_time):
    #print(f"Value: {report(dmm)}")
    #print(f"current_time = ", current_time)
    line = [current_time, report(dmm)]

    with open("log0" + str(log_num) + ".csv", "a") as log_file:
        log_writer = csv.writer(log_file,dialect='excel' )#,quoting= csv.QUOTE_NONNUMERIC)
        log_writer.writerow(line)

    current_time = (time.clock_gettime(time.CLOCK_BOOTTIME)) - start_time
    time.sleep(sampling_period)


