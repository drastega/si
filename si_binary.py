#!/usr/bin/python
import numpy as np
import sys, os, time
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from IPython import embed
tstart = time.time()
### my functions from separate files
from si_func_ps_dark_flat import si_func_ps_dark_flat
from si_func_ps_diff import si_func_ps_diff
###

data_filename = sys.argv[1]
middle_dark_filename = sys.argv[2]
frame_size_bytes = 512*512*2 # 524288 bytes
data_size_bytes = os.stat(data_filename).st_size

if len(sys.argv) < 4:
    frame_number = data_size_bytes / frame_size_bytes
else:
    frame_number = int(sys.argv[3])

f = open(data_filename, 'rb')
data_size_bytes = frame_number * frame_size_bytes
data = np.frombuffer(f.read(data_size_bytes), dtype=np.uint16).reshape((frame_number,512,512))
f.close

middle_dark = np.load(middle_dark_filename)

frame = data[0,...]
#ps = si_func_ps_dark_flat(data, middle_dark, frame_number)
ps, max_counts = si_func_ps_diff(data, frame_number)

del data
acf = np.abs(np.fft.fftshift(np.fft.ifft2(ps)))
phase = np.angle(np.fft.fftshift(np.fft.ifft2(frame)))

y,x = np.histogram(max_counts, bins=2000)

print '###################################'
print 'Number of frames is ', frame_number
print 'Time of ps calculation is ' , round((time.time()-tstart)/60., 1), ' min'
print '###################################'

################################### Visualization
app = QtGui.QApplication([])
## Create window with four ImageView widgets
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
win = QtGui.QMainWindow()
win.resize(1200,800)
win.setWindowTitle('Speckle interferometry of '+data_filename)
cw = QtGui.QWidget()
win.setCentralWidget(cw)
l = QtGui.QGridLayout()
cw.setLayout(l)
imv1 = pg.ImageView()
imv2 = pg.ImageView()
imv3 = pg.ImageView()
#imv4 = pg.PlotWidget()
imv4 = pg.ImageView()
l.addWidget(imv1, 0, 0)
l.addWidget(imv2, 0, 1)
l.addWidget(imv3, 1, 0)
l.addWidget(imv4, 1, 1)
win.show()

imv1.setImage(frame)
imv1.setLevels(300, 2000)
imv1.normRoi.hide()
imv2.setImage(ps/1e7)
imv2.setLevels(1e7, 1e8)
imv3.setImage(acf)
imv3.setLevels(0, 3e12)
imv4.setImage(phase)

#curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 255), pen={'color': 'k'})
#imv4.addItem(curve)
#imv4.plot(max_counts, pen={'color': 'k'})

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
###################################
#embed()
