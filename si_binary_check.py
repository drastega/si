#!/usr/bin/python
import numpy as np
import sys, os, time
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from IPython import embed
tstart = time.time()
### my functions from separate files
from si_func_ps_diff import si_func_ps_diff
###

data_filename = sys.argv[1]
frame_size_bytes = 512*512*2 # 524288 bytes
data_size_bytes = os.stat(data_filename).st_size

if len(sys.argv) < 3:
    frame_number = data_size_bytes / frame_size_bytes
else:
    frame_number = int(sys.argv[2])

f = open(data_filename, 'rb')
data_size_bytes = frame_number * frame_size_bytes
data = np.frombuffer(f.read(data_size_bytes), dtype=np.uint16).reshape((frame_number,512,512))
f.close

frame = data[0,...]
ps, avg = si_func_ps_diff(data, frame_number)
del data
acf = np.abs(np.fft.fftshift(np.fft.ifft2(ps)))

print '###################################'
print 'Number of frames is ', frame_number
print 'Time of calculation is ' , round((time.time()-tstart)/60., 1), ' min'
print '###################################'

################################### Visualization
app = QtGui.QApplication([])
## Create window with four ImageView widgets
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

win = QtGui.QMainWindow()
win.resize(1200,800)
win.setWindowTitle('Qualitative speckle interferometry of '+data_filename)
cw = QtGui.QWidget()
win.setCentralWidget(cw)
l = QtGui.QGridLayout()
cw.setLayout(l)
imv1, imv2, imv3, imv4 = pg.ImageView(), pg.ImageView(), pg.ImageView(), pg.ImageView()
l.addWidget(imv1, 0, 0), l.addWidget(imv2, 0, 1), l.addWidget(imv3, 1, 0), l.addWidget(imv4, 1, 1)
win.show()

imv1.setImage(frame, levels=(300, 2000)), imv1.ui.normBtn.hide()
imv2.setImage(avg), imv2.ui.normBtn.hide()
imv3.setImage(ps/1e7, levels=(1e7, 1e8)), imv3.ui.normBtn.hide()
imv4.setImage(acf), imv4.ui.normBtn.hide()

text = pg.TextItem("Seeing is")#, anchor=(0.0, 0.0))
text.setPos(20.0, 5.0)
imv2.addItem(text)

## Start the Qt event loop
app.exec_()
###################################
#embed()
