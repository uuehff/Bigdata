# -*- coding: utf-8 -*-
import random

from echarts import Echart, Series, Toolbox, Tooltip, Legend, VisualMap


def randomData():
    return random.randint(1,999)


chart = Echart('iphone销量','纯属虚构', axis=False) # 不使用axis选项

# chart.use(Tooltip(trigger='item'))
# chart.use(Legend(['iphone3','iphone4','iphone5'],orient='vertical',left='left',itemWidth=45,itemHeight=20))
# chart.use(VisualMap('continuous',min=0,max=2500,text=['高','低'],calculable=True,left=10,bottom=10))
# chart.use(Toolbox(show='true',orient='vertical',position='top'))

# iphon3_data = [{"name": '北京',"value": 1000},{"name": '天津',"value": 500},{"name": '上海',"value": 250}]
# iphon4_data = [{"name": '北京',"value": 500},{"name": '天津',"value": 300}]
# iphon5_data = [{"name": '北京',"value": 200}]

iphon3_data =   [
                {"name": '北京',"value": randomData() },
                {"name": '天津',"value": randomData() },
                {"name": '上海',"value": randomData() },
                {"name": '重庆',"value": randomData() },
                {"name": '河北',"value": randomData() },
                {"name": '河南',"value": randomData() },
                {"name": '云南',"value": randomData() },
                {"name": '辽宁',"value": randomData() },
                {"name": '黑龙江',"value": randomData() },
                {"name": '湖南',"value": randomData() },
                {"name": '安徽',"value": randomData() },
                {"name": '山东',"value": randomData() },
                {"name": '新疆',"value": randomData() },
                {"name": '江苏',"value": randomData() },
                {"name": '浙江',"value": randomData() },
                {"name": '江西',"value": randomData() },
                {"name": '湖北',"value": randomData() },
                {"name": '广西',"value": randomData() },
                {"name": '甘肃',"value": randomData() },
                {"name": '山西',"value": randomData() },
                {"name": '内蒙古',"value": randomData() },
                {"name": '陕西',"value": randomData() },
                {"name": '吉林',"value": randomData() },
                {"name": '福建',"value": randomData() },
                {"name": '贵州',"value": randomData() },
                {"name": '广东',"value": randomData() },
                {"name": '青海',"value": randomData() },
                {"name": '西藏',"value": randomData() },
                {"name": '四川',"value": randomData() },
                {"name": '宁夏',"value": randomData() },
                {"name": '海南',"value": randomData() },
                {"name": '台湾',"value": randomData() },
                {"name": '香港',"value": randomData() },
                {"name": '澳门',"value": randomData() }
            ]

iphon4_data =   [
                {"name": '北京',"value": randomData() },
                {"name": '天津',"value": randomData() },
                {"name": '上海',"value": randomData() },
                {"name": '重庆',"value": randomData() },
                {"name": '河北',"value": randomData() },
                {"name": '安徽',"value": randomData() },
                {"name": '新疆',"value": randomData() },
                {"name": '浙江',"value": randomData() },
                {"name": '江西',"value": randomData() },
                {"name": '山西',"value": randomData() },
                {"name": '内蒙古',"value": randomData() },
                {"name": '吉林',"value": randomData() },
                {"name": '福建',"value": randomData() },
                {"name": '广东',"value": randomData() },
                {"name": '西藏',"value": randomData() },
                {"name": '四川',"value": randomData() },
                {"name": '宁夏',"value": randomData() },
                {"name": '香港',"value": randomData() },
                {"name": '澳门',"value": randomData() }
            ]

iphon5_data =   [
                {"name": '北京',"value": randomData() },
                {"name": '天津',"value": randomData() },
                {"name": '上海',"value": randomData() },
                {"name": '广东',"value": randomData() },
                {"name": '台湾',"value": randomData() },
                {"name": '香港',"value": randomData() },
                {"name": '澳门',"value": randomData() }
            ]

# chart.use(Series(type='map',name='iphone3',data=iphon3_data,map='china',roam=False,label={"normal":{"show":True},"emphasis":{"show":True}}))
# chart.use(Series(type='map',name='iphone4',data=iphon4_data,map='china',roam=False,label={"normal":{"show":True},"emphasis":{"show":True}}))
# chart.use(Series(type='map',name='iphone5',data=iphon5_data,map='china',roam=False,label={"normal":{"show":True},"emphasis":{"show":True}}))
#画词云图
chart.use(Series('wordCloud','hello',iphon5_data,
                 gridSize=20,
                 sizeRange=[12,50],
                 rotationRange=[0,0],
                 shape='circle',
                 textStyle={"normal":{"color":'#aaa'},"emphasis":{"shadowBlur":10,"shadowColor":'#333'}}))

# chart.plot()
chart.save("./tupian/","china18")
