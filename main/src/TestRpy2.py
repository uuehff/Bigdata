# -*- coding: utf-8 -*-
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr,data
import os
import math,datetime


rprint = robjects.globalenv.get("print")
stats = importr('stats')
grdevices = importr('grDevices')
base = importr('base')
datasets = importr('datasets')

#画图1
mtcars = data(datasets).fetch('mtcars')['mtcars']
gp = ggplot2.ggplot(mtcars)
pp = gp + \
     ggplot2.aes_string(x='wt', y='mpg') + \
     ggplot2.geom_point()

pp.plot()

#画图2
# r = robjects.r
# x = robjects.IntVector(range(10))
# y = r.rnorm(10)
# r.X11()
# r.layout(r.matrix(robjects.IntVector([1,2,3,2]), nrow=2, ncol=2))
# r.plot(r.runif(10), y, xlab="runif", ylab="foo/bar", col="red")




