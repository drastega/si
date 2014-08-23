#!/usr/bin/python
import numpy as np
import pyqtgraph as pg
import os, sys
#from IPython import embed

data_path = sys.argv[1]
data_name_ext = os.path.basename(data_path)
data_name = os.path.splitext(data_name_ext)[0]

def avg_img(file_path):
    frame_size_bytes = 512*512*2 # 524288 bytes
    data_size_bytes = os.stat(file_path).st_size
    N = data_size_bytes / frame_size_bytes
    avg = np.zeros((512,512),np.float)
    f = open(file_path, 'rb')
    for i in range(N):
        image = np.frombuffer(f.read(frame_size_bytes), dtype=np.uint16).reshape((512,512))
        avg = avg + image/float(N)
        print i
    f.close
    return avg

avg_data = avg_img(data_path)

np.save('./avg_'+data_name,avg_data)

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
imv = pg.image(avg_data, title = "Average data")
imv.ui.normBtn.hide()

text = pg.TextItem("here")#, anchor=(0.0, 0.0))
text.setPos(1.0, 5.0)
imv.addItem(text)

exporter = pg.exporters.ImageExporter.ImageExporter(imv.ImageView)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

#embed() # to call ipython
