#!/usr/bin/python
'''
This program computes average power spectrum of speckle data (in .dat format)
for a given number of frames (all frames by default) using adjacent frames difference
instead of average dark subtraction.
'''
import numpy as np

def si_func_ps_diff(data_cube_np_array, frame_number):
    image = np.zeros((1024,1024),np.float)
    ps = np.zeros((1024,1024),np.float)
#    max_counts = []
    avg = np.zeros((512,512),np.float)
    for i in range(1, frame_number):

        image[:512,:512] = data_cube_np_array[i,:,:] - data_cube_np_array[i-1,:,:]
        image[:512,:512] = image[:512,:512] - image[:512,:512].mean()
#        max_counts.append(image.max())
        image_ps = np.abs(np.fft.fft2(image))**2
        ps += image_ps
        avg = avg + data_cube_np_array[i-1,:,:]/float(frame_number)
        print 'Frame #', i, 'mean', image[:512,:512].mean()

    ps = np.fft.fftshift(ps) / (frame_number - 1)
    return ps, avg
