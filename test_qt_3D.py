#!/usr/bin/python
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import scipy.ndimage as ndi
import numpy as np
import math

## Create a GL View widget to display data
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
w.setCameraPosition(distance=50)

theta = math.radians(-10)
freq = 1
amplitude = 10
s=512
z = np.fromfunction(lambda x,y: amplitude*np.sin(freq*(x*np.cos(theta) + y*np.sin(theta))), (50,50))
#z = np.load('/Users/leda/.Home/programs/python/SI/2014-07-14/acf.npy')
x = np.linspace(0,49, 50)
y = np.linspace(0,49, 50)
p1 = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='normalColor')
#p1.translate(-10,-10,0)
w.addItem(p1)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
