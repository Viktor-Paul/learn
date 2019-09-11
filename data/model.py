import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as mp
import matplotlib.dates as md
import pandas as pd

class StockPredictionModel(object):
    def __init__(self, kdata):
        self.kdata = kdata

    def analysis(self):
        result_dict = {0:self.by_trendline(), 1:self.by_boll(), 2:by_obv(), 3:by_ma()}
        result_final = predict()
        return {'result':result_final, 'data':result_dict}

    def by_obv(self):
        pass

    def by_trendline(self):
        return '整体处于上涨趋势，建议继续持有。'

    def by_boll(self):
         return '股价没有太大波动，建议持有。'

    def by_ma(self):
        return '均线理论建议结果。'


header = ['date','open','high','low','close','volume','ma5','ma10','ma20']
kdata = pd.read_csv('k_data.csv', names=header, parse_dates=[0], index_col=0)
for i in range(100):
    model = StockPredictionModel(kdata[i:i+9][::-1])
    print(model.by_boll())