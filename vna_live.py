# open a anaconda prompt, move to c:\xampp\htdocs\vna_live and type
# python vna_live.py
import time
import pyvisa
import os
import json
import numpy as np

rm = pyvisa.ResourceManager()
vna_gpib = rm.open_resource('GPIB1::19::INSTR')

while True:
    f_start = float(vna_gpib.query('SENS:FREQ:STAR?'))
    f_stop = float(vna_gpib.query('SENS:FREQ:STOP?'))
    npts = int(vna_gpib.query('SENS:SWE:POIN?'))
    frequency = np.linspace(f_start,f_stop,npts);

    power = float(vna_gpib.query('SOUR:POW1?'))
    rbw = float(vna_gpib.query('sense:bandwidth:resolution?'))

    vna_gpib.write('CALCulate:PARameter:SELect "CH1_S12_2"')
    vna_gpib.write('FORMat ASCII, 0')
    rawdata = vna_gpib.query('CALCulate:DATA? FDATA')
    asciiarray = rawdata.split(',')
    data = []
    for element in asciiarray:
        converted_float = float(element)
        data.append(converted_float)

    jsondata = json.loads('{}')
    jsondata['S21_logmag'] = data
    jsondata['frequency'] = frequency.tolist()
    jsondata['notes'] = "test data"
    jsondata['power'] = power
    jsondata['resolution_bandwidth'] = rbw
    jsondata['npts'] = npts
    jsondata['f_start'] = f_start
    jsondata['f_stop'] = f_stop
    jsondata['timestamp'] = int(time.time())
    jsonstring = json.dumps(jsondata, indent=2)

    filename = "testdata.txt"
    jsonstring = json.dumps(jsondata)
    file = open(filename, 'w')
    file.write(jsonstring)
    file.close()    
    time.sleep(0.01)