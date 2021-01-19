#!/usr/bin/python3
import serial
import time

dmm = None
dmm = serial.Serial(port="/dev/ttyS0", baudrate=115200, timeout=0.005)

def report(dmm):
    if dmm:
        dmm.write(b"read? buf\r")
        line = dmm.readline().decode("utf-8")
        # print(f"RX: {line}")
        
        reply_list = line.split(',')
        str_value = reply_list[0].lower()
        # print(f"{str_value}")
        return float(str_value)

while(True):
    print(f"Value: {report(dmm)}")
    time.sleep(0.005)