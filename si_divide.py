#!/usr/bin/python
import numpy as np
import pyqtgraph as pg
import sys
#from IPython import embed

data1_path = sys.argv[1]
data2_path = sys.argv[2]

data1 = np.load(data1_path)
data2 = np.load(data2_path)

quotient = data1 / data2

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
imv = pg.image(quotient, title = data1_path+"/"+data2_path)
imv.ui.normBtn.hide()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()

#embed() # to call ipython
