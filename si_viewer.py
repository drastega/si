#!/usr/bin/python
'''
This is a program for visualization of different kind of SI data
Usage:
 si_viewer.py filename
Examples:
 si_viewer.py hd65339_800.dat
 si_viewer.py acf.npy 
 si_viewer.py ps.npy
 si_viewer.py avg_dark1.npy
 si_viewer.py dark1.dat
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pyqtgraph as pg
import sys, os
from IPython import embed

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

data_path = sys.argv[1]
########################### PS or ACF visualization #####################
if os.stat(data_path).st_size < 10000000: # Checking file size
    data = np.load(data_path)
    data_title = data_path
    if data.max() > 1e12:
        data = data / 1e7
        data_title = 'Data / 1e7'
    imv = pg.image(data, title = data_title)
    imv.ui.normBtn.hide()
#    imv.roi.setPen(pen={'width': 1.3})
#    imv.roiCurve.setPen(pen={'color': 'r'})
    
## Start Qt event loop unless running in interactive mode or using pyside.
    if __name__ == '__main__':
        import sys
        if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
            pg.QtGui.QApplication.exec_()

#### To save image
    if raw_input('Do you want to save image? y/[n]: ') == 'y':
        data_min = input('Enter min value: ')
        data_max = input('Enter max value: ')
        data = np.rot90(data)
        plt.imshow(data, vmin=data_min, vmax=data_max, origin='lower', cmap='jet')
        plt.colorbar()
        plt.savefig('data.pdf', transparent=True)

########################### Image slicer for raw data #####################
else:
    f = open(data_path, 'rb')
    frame_number = os.stat(data_path).st_size / (512*512*2)
    data = np.fromfile(file=f, dtype=np.uint16).reshape((frame_number,512,512))

    ax = plt.subplot(111)
    plt.subplots_adjust(left=0.2, bottom=0.2)

    frame = 0
    l = plt.imshow(data[frame,:,:])#, origin = 'lower') #shows 0th frame
    plt.xticks(range(100,501,100),range(100,501,100))
    plt.title(data_path)
    axframe = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg='lightgoldenrodyellow')
    sframe = Slider(axframe, 'Frame', 0, frame_number-1, valinit=0, valfmt='%1.0f')

    def update(val):
        frame = np.around(sframe.val)
        l.set_data(data[frame,:,:])

    sframe.on_changed(update)
    plt.show()

#### To save image
    if raw_input('Do you want to save a frame? y/[n]: ') == 'y':
        frame_number = input('Enter frame number: ')
        data = data[frame_number-1,...]
        imv = pg.image(data)
        imv.ui.normBtn.hide()
## Start Qt event loop unless running in interactive mode or using pyside.
        if __name__ == '__main__':
            import sys
            if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
                pg.QtGui.QApplication.exec_()
##
        data_min = input('Enter min value: ')
        data_max = input('Enter max value: ')
#        data = np.rot90(data)
        plt.imshow(data, vmin=data_min, vmax=data_max)#, origin='lower', cmap='jet')
        plt.colorbar()
        plt.savefig('data.jpeg', transparent=True)
#embed() # uncomment to call ipython
