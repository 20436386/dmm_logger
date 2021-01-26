# dmm_logger
Log for DMM
In order to log data from the GWINSTEK GDM-8261A the configuration must be done on the actual multimeter before you execute the program. 
In order to increse the sampling rate to its maximum, set the sampling rate to fast on the actually multimeter before you run the program.
after this is done it appears that the maximum sampling rate is around 10 milliseconds. note that the maximum sampling rate if the tracking 
function is selected is 30 milliseconds(this is due to the refresh rate of matplotlib), the data can however be saved to a .csv file for sampling rates up to 10 milliseconds.
run ./serial_sceleton.py --help for more information on the arguments taken in
