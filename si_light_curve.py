#!/usr/bin/python
import numpy as np
import pyqtgraph as pg
import os, sys
#from IPython import embed

data_path = sys.argv[1]
data_name_ext = os.path.basename(data_path)
data_name = os.path.splitext(data_name_ext)[0]

lc = []
def light_curve(file_path):
    frame_size_bytes = 512*512*2 # 524288 bytes
    data_size_bytes = os.stat(file_path).st_size
    N = data_size_bytes / frame_size_bytes
    f = open(file_path, 'rb')
    for i in range(N):
        image = np.frombuffer(f.read(frame_size_bytes), dtype=np.uint16).reshape((512,512))
        lc.append(image.sum())
        print i
    f.close
    return lc

lc = light_curve(data_path)
#np.save('./lc_'+data_name,lc)

#pg.setConfigOption('background', 'w')
#pg.setConfigOption('foreground', 'k')
pg.plot(lc, title = "Light curve of "+data_name)#, pen={'color': 'k'})

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

#embed() # to call ipython
