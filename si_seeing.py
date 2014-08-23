#!/usr/bin/python
import numpy as np
import sys, os, time
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from scipy import ndimage
from fit_2D_gaussian import *
from IPython import embed
tstart = time.time()

def si_avg(data_cube_np_array, frame_number):
    xc, yc = [], []
    avg = np.zeros((512,512),np.float)
    avg_centered = np.zeros((512,512),np.float)
    for i in range(frame_number):
        x, y = ndimage.measurements.center_of_mass(data_cube_np_array[i,:,:])
#        xc.append(x), yc.append(y)
        avg = avg + data_cube_np_array[i,:,:]/float(frame_number)
        frame = np.roll(data_cube_np_array[i,:,:], 255-np.int(x), axis=1)
        frame = np.roll(frame, 255-np.int(y), axis=0)
        avg_centered = avg_centered + frame/float(frame_number)
        print 'Frame #', i
    return avg, avg_centered

data_filename = sys.argv[1]
frame_size_bytes = 512*512*2 # 524288 bytes
data_size_bytes = os.stat(data_filename).st_size
frame_number = data_size_bytes / frame_size_bytes
f = open(data_filename, 'rb')
#data_size_bytes = frame_number * frame_size_bytes
data = np.frombuffer(f.read(data_size_bytes), dtype=np.uint16).reshape((frame_number,512,512))
f.close
frame = data[0,...]
avg, avg_centered = si_avg(data, frame_number)
del data
print '###################################'
print 'Number of frames is ', frame_number
print 'Time of calculation is ' , round((time.time()-tstart), 1), ' sec'
print '###################################'

params = fitgaussian(avg)
fit = gaussian(*params)
print params
height, center_x, center_y, width_x, width_y = params
center_x += 256
center_y += 256
#tmp = np.fromfunction(lambda x,y: height*np.exp(-(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2), (1024,1024))
tmp = np.fromfunction(lambda x,y: np.sin(0.1*(x+y)), (512,512))
################################### Visualization
app = QtGui.QApplication([])
## Create window with four ImageView widgets
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

STEPS = np.array([0.0, 0.33, 0.66, 1.0])
CLRS = ['k', 'r', 'y', 'w']
clrmp = pg.ColorMap(STEPS, np.array([pg.colorTuple(pg.Color(c)) for c in CLRS]))

win = QtGui.QMainWindow()
win.show()
win.resize(900,900)
win.setWindowTitle('Seeing of '+data_filename)

cw = QtGui.QWidget()
win.setCentralWidget(cw)
l = QtGui.QGridLayout()
cw.setLayout(l)
imv1, imv2, imv3, imv4 = pg.ImageView(), pg.ImageView(), pg.ImageView(), pg.ImageView()
l.addWidget(imv1, 0, 0), l.addWidget(imv2, 0, 1), l.addWidget(imv3, 1, 0), l.addWidget(imv4, 1, 1)

imv1.setImage(frame, levels=(300, 2000)), imv1.ui.normBtn.hide(), imv1.ui.histogram.gradient.setColorMap(clrmp)
imv2.setImage(avg), imv2.ui.normBtn.hide(), imv2.ui.histogram.gradient.setColorMap(clrmp)
imv3.setImage(avg_centered), imv3.ui.normBtn.hide()#, imv3.ui.histogram.gradient.setColorMap(clrmp)
imv4.setImage(avg), imv4.ui.normBtn.hide()#, imv4.ui.histogram.gradient.setColorMap(clrmp)

#imv4.setFixedWidth(400)
#imv4.setFixedWidth(370), imv4.setFixedHeight(370), imv4.setTitle(title="Distribution of image's centers")
#imv3.setImage(ps/1e7, levels=(1e7, 1e8)), imv3.ui.normBtn.hide()
#imv4.setImage(acf), imv4.ui.normBtn.hide()

#sct_item = pg.ScatterPlotItem(size=1)
#sct_item.setData(xc,yc,pen={'color': 'b'})
#imv4.addItem(sct_item)
#imv4.setXRange(0,512)
#imv4.setYRange(0,512)

#text = pg.TextItem("Seeing is")
#text.setPos(20.0, 5.0)
#imv2.addItem(text)

#win.show()
## Start the Qt event loop
app.exec_()
###################################
#embed()
