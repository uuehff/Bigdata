# encoding:utf-8
from __future__ import print_function
import numpy as np
# 计算相关系数
import pandas as pd
filename = '../data/tieba_corr.xls'
data = pd.read_excel(filename, index_col=u'贴吧名称')  # 读取数据，指定“贴吧名称”列为索引列
# print(data[u'文章数'])
corr = data.corr()
print(corr)
a=[[1.000000,0.351485,0.514088,0.521088],
   [0.351485,1.000000,0.931497,0.935789],
   [0.514088,0.931497,1.000000,0.999789],
   [0.521088,0.935789,0.999789,1.000000]]
print(a)
# 画热图
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
def draw_heatmap(data,xlabels,ylabels):
    cmap = cm.Blues  # 纯色
    # cmap = cm.get_cmap('rainbow', 1000)
    figure=plt.figure(facecolor='w')
    ax=figure.add_subplot(2,1,1,position=[0.1,0.15,0.8,0.8])
    ax.set_yticks(range(len(ylabels)))
    ax.set_yticklabels(ylabels)
    ax.set_xticks(range(len(xlabels)))
    ax.set_xticklabels(xlabels)
    vmax=data[0][0]
    vmin=data[0][0]
    for i in data:
        for j in i:
            if j>vmax:
                vmax=j
            if j<vmin:
                vmin=j
    map=ax.imshow(data,interpolation='nearest',cmap=cmap,aspect='auto',vmin=vmin,vmax=vmax)
    cb=plt.colorbar(mappable=map,cax=None,ax=None,shrink=0.5)
    plt.title(u'贴吧数据相关度热图')
    plt.show()
xlabels = [u'文章数',u'总评论数',u'关注数',u'帖子数']
ylabels = [u'文章数',u'总评论数',u'关注数',u'帖子数']

draw_heatmap(a,xlabels,ylabels)