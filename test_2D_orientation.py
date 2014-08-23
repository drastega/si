#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from IPython import embed

image = np.ones((256,256),np.float)
image *= np.arange(256)
image = image.T
print image

#################### Matplotlib
plt.imshow(image, cmap='gray')
#plt.show()
#plt.imshow(np.rot90(image), cmap='gray')

#################### PyQtGraph
pg.setConfigOption('background', 'g')
pg.setConfigOption('foreground', 'k')

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Create main window with a grid layout inside
win = QtGui.QMainWindow()
win.resize(700,700)
win.setWindowTitle('Test')

## Define a top-level widget to hold everything
w = QtGui.QWidget()
win.setCentralWidget(w)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## 
imgView = pg.ImageView(view=pg.PlotItem())
layout.addWidget(imgView)#, 0, 0)
imgView.setImage(image)
imgView.ui.normBtn.hide()
imgView.setFixedSize(600,600)

STEPS = np.array([0.0, 0.33, 0.66, 1.0])
CLRS = ['k', 'r', 'y', 'w']
clrmp = pg.ColorMap(STEPS, np.array([pg.colorTuple(pg.Color(c)) for c in CLRS]))

imgView.ui.histogram.gradient.setColorMap(clrmp)
#imgView.ui.roiPlot.setFixedSize(200,100)
imgView.ui.roiPlot.setLineWidth((30))

#pg.image(np.rot90(image))
win.show()
app.exec_()

embed()
