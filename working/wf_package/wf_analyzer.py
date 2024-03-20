#!/usr/bin/env python

import struct
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import struct
import multiprocessing, pathos.multiprocessing
from tqdm.notebook import tqdm
import os
import time

def read_channel(channel_file):
  """Read a binary file and create an array of waveforms"""
  with open(channel_file, "rb") as file:
        binary_data = file.read()
        uint16_data = struct.unpack('<' + 'H' * (len(binary_data) // 2), binary_data)
        y = np.array(uint16_data)
        ticks = memorydepth
        wfs = y.reshape(len(y)//ticks, ticks).astype(float)
     
     return wfs

def sub_baseline(wfs, pre_pulse):
  """Subtract the baseline to all the waveform sampling the first pre_pulse
  ticks"""
   for wf in wfs:
        baseline = (np.sum(wf[0:pre_pulse]))/pre_pulse
        wf -= baseline 
     
     return -wfs



def build_template(wfs):
  """Buil the template for a matched filter"""
    n = 0.
    avg = np.zeros(memorydepth).astype(float)
    for wf in wfs:
        avg += wf
        n += 1
    n = 1/n
    avg = avg*n
    template = np.flip(avg)
    
    return template

def build_calib_spectrum(wfs, template, int_low, int_up):
  """Buil the calibration spectrum by integratin in the window [int_low; int_up]"""
    int_wf = np.empty(shape=(0,)).astype(float)
    for wf in wfs:
        filtered_wf = signal.convolve(wf, template)
        int_wf = np.append(int_wf, get_wf_integral(filtered_wf, int_low, int_up))
    return int_wf

def avg_wf(wfs, template):
  """Apply a mathced filter and average the filtered wavewforms"""
    n = 0.
    avg = np.zeros(memorydepth+len(template)-1).astype(float)
    for wf in wfs:
        avg += signal.convolve(wf, template)
        n += 1
    n = 1/n
    avg = avg*n
    
    return avg

def zero_crossings(arr):
    """Find the zero-crossing of an array"""
    signs = np.sign(arr)
    zero_crossings_indices = np.where(np.diff(signs))[0]
    
    # Interpolate zero-crossings
    zero_crossings_points = []
    for idx in zero_crossings_indices:
        if signs[idx] == 0:  # Handle exactly zero points
            zero_crossings_points.append(idx)
        else:
            # Linear interpolation between adjacent points
            x1, x2 = idx, idx + 1
            y1, y2 = arr[x1], arr[x2]
            zero_crossings_points.append(x1 - y1 * (x2 - x1) / (y2 - y1))
    
    return zero_crossings_points
