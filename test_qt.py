#!/usr/bin/python
from PyQt4 import QtGui  # (the example applies equally well to PySide)
import pyqtgraph as pg
from IPython import embed

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()

## Create some widgets to be placed inside
btn = QtGui.QPushButton('press me')
text = QtGui.QLineEdit('enter text')
#listw = QtGui.QListWidget()
plot = pg.PlotWidget()
imv = pg.ImageView()
plot.setFixedHeight(500)
plot.setFixedWidth(500)
imv.setFixedWidth(500)
imv.setFixedHeight(500)


## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)

## Add widgets to the layout in their proper positions
#layout.addWidget(btn, 0, 0)   # button goes in upper-left
#layout.addWidget(text, 1, 0)   # text edit goes in middle-left
layout.addWidget(plot, 0, 0)  # list widget goes in bottom-left
layout.addWidget(imv, 0, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

## Start the Qt event loop
app.exec_()
#embed()
