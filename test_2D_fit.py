#!/usr/bin/python
import numpy as np
import math
import pyqtgraph as pg

theta = math.radians(-10)
freq = 0.1
frame = np.fromfunction(lambda x,y: np.sin(freq*(x*np.cos(theta) + y*np.sin(theta))), (512,512))

#frame = np.fromfunction(lambda x,y: np.sin(0.2*(x+0.1*y)), (512,512))

height = 2
center_x = 255
center_y = 255
width_x = 40
width_y = 80

gauss = np.fromfunction(lambda x,y: height*np.exp(-(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2), (512,512))

pg.image(frame*gauss)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
