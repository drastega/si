#!/usr/bin/python
import numpy as np
import pyqtgraph as pg
import os, sys
from IPython import embed

data_path = sys.argv[1]
data_name_ext = os.path.basename(data_path)
data_name = os.path.splitext(data_name_ext)[0]

def max_counts(file_path):
    frame_size_bytes = 512*512*2 # 524288 bytes
    data_size_bytes = os.stat(file_path).st_size
    N = data_size_bytes / frame_size_bytes
    max_count = []
    f = open(file_path, 'rb')
    for i in range(N):
        image = np.frombuffer(f.read(frame_size_bytes), dtype=np.uint16)#.reshape((512,512))
        max_count.append(image.max())
        print "max count in "+str(i+1)+"-th frame =", image.max()
    f.close
    return max_count

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

max_count_list = max_counts(data_path)
y,x = np.histogram(max_count_list, bins=2000)

win = pg.GraphicsWindow()
win.resize(1000,330)
win.setWindowTitle('Stat of max counts in ' + data_name)
plt1 = win.addPlot()
plt2 = win.addPlot()
#imv = win.addViewBox()
#imv.image(np.random.random_sample((512, 512)))
curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 255), pen={'color': 'k'})
plt1.addItem(curve)
plt2.plot(max_count_list, pen={'color': 'k'})

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

embed() # to call ipython
