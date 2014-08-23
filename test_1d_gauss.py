#!/usr/bin/python
from pylab import *

gaussian = lambda x: 30*exp(-(30-x)**2/20.)
data = gaussian(arange(100))
#plot(data)

height = 800.
center_x = 256.
center_y = 256.
width_x = 30.
width_y = 50.
gauss2D = lambda x, y: height*exp(-(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

data_x = gauss2D(arange(100))#,arange(100))
print data_x.shape#, data_y.shape

'''
X = arange(data.size)
x = sum(X*data)/sum(data)
width = sqrt(abs(sum((X-x)**2*data)/sum(data)))

max = data.max()

fit = lambda t : max*exp(-(t-x)**2/(2*width**2))

plot(fit(X))
'''
show()
