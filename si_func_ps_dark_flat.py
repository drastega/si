#!/usr/bin/python
import numpy as np

def si_func_ps_dark_flat(data_cube_np_array, middle_dark, frame_number):
    image = np.zeros((1024,1024),np.float)
    ps = np.zeros((1024,1024),np.float)
    for i in range(frame_number):
        image[:512,:512] = data_cube_np_array[i,:,:] - middle_dark
        image[:512,:512] = image[:512,:512] - image[:512,:512].mean()
        image_ps = np.abs(np.fft.fft2(image))**2
        ps += image_ps
        print 'Frame #', i, 'mean', image[:512,:512].mean()
    ps = np.fft.fftshift(ps) / frame_number
    return ps
