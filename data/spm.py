import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as mp
import matplotlib.dates as md
import pandas as pd

class StockPredictionModel(object):
    ''' 股价预测模型
    当前类根据传入的某支股票K线数据进行量化分析，从股价趋势线、布林带、OBV、
    5日移动均线、10日移动均线等指标分析后得出分析结果，最终给出建议：买入、卖出、持有

    Attributes:
        kdata:  存储当前股票每天的k线数据，结构如下：
                |date|open|high|low|close|volume|ma5|ma10|ma20|
                date: 交易日期
                opening_price: 开盘价
                highest_price: 最高价
                lowest_price:  最低价
                closing_price: 收盘价
                volume:        当日交易量
                ma5:           5日均线
                ma10:          10日均线
                ma20:          20日均线
    '''
    def __init__(self, kdata):
        '''
        kdata 当前股票数据
        '''
        self.kdata = kdata

    def analysis(self):
        '''分析当前股票的kdata，得出不同指标下的结论，返回分析结果。
            dic: {0:'从股价趋势线分析，看涨.', 1:'从布林带分析，看跌.' ......}
                0: 股价趋势线指标结果
                1: 布林带指标结果
                2: OBV指标结果
                3: 移动均线指标结果
        '''
        result_dict = {0:self.by_trendline(), 1:self.by_boll(), 2:by_obv(), 3:by_ma()}
        result_final = predict()
        return {'result':result_final, 'data':result_dict}

    def by_obv(self):
        pass

    def by_trendline(self):
        kdata = self.kdata
        dates = kdata.index
        highest_prices = kdata['high']
        lowest_prices = kdata['low']
        closing_prices = kdata['close']
        trend_points = (highest_prices + lowest_prices + closing_prices) / 3
        days = (pd.Series(dates) - pd.to_datetime('1970')).dt.days
        a = np.column_stack((days, np.ones_like(days)))
        x = np.linalg.lstsq(a, trend_points)[0]
        trend_k = x[0]
        if trend_k >= 0:  # 上涨趋势
            trend_points = lowest_prices
            days = (pd.Series(dates) - pd.to_datetime('1970')).dt.days
            a = np.column_stack((days, np.ones_like(days)))
            x = np.linalg.lstsq(a, trend_points)[0]
            last3daysx = days[-2:]
            last3daysy = last3daysx * x[0] + x[1]
            print(closing_prices[-2:])
            if np.all(np.array(closing_prices[-2:]) < np.array(last3daysy)):
                return '上涨趋势下，最近两日跌破趋势线，建议卖出。'
            else:
                return '整体处于上涨趋势，建议继续持有。'

        if trend_k < 0:  # 下跌趋势
            trend_points = highest_prices
            days = (pd.Series(dates) - pd.to_datetime('1970')).dt.days
            a = np.column_stack((days, np.ones_like(days)))
            x = np.linalg.lstsq(a, trend_points)[0]
            last3daysx = days[-2:]
            last3daysy = last3daysx * x[0] + x[1]
            print(closing_prices[-2:])
            if np.all(np.array(closing_prices[-2:]) > np.array(last3daysy)):
                return '下跌趋势下，最近三日冲破趋势线，建议买入。'
            else:
                return '整体处于下跌趋势，建议观察。'

    
    '''
    布林带
    中轨往往是一条加权均线
    上轨和下轨分别是中轨加上或减去同期收盘价的标准差的2倍
    '''
    def by_boll(self):
        kdata = self.kdata
        dates = kdata.index
        closing_prices = kdata['close']
        ma5 = kdata['ma5']
        # 求标准差
        stds = np.zeros(ma5.size - 4)
        for i in range(0, stds.size):
            stds[i] = closing_prices[i:i + 5].std()
        lower = ma5[4:] - 2*stds
        upper = ma5[4:] + 2*stds
        # 穿透布林带
        print(closing_prices[-2:])
        if np.all(closing_prices[-2:] > upper[-2:]):
            return '上涨趋势穿透布林带顶部压力线，建议卖出。'
        elif np.all(closing_prices[-2:] < lower[-2:]):
            return '下跌趋势穿透布林带底部支撑线，建议买入。'
        # 在布林带中震荡
        if ((closing_prices[-10:] > ma5[-10:]).sum()>6) and (closing_prices[-1]<ma5[-1]) and (closing_prices[-2]>ma5[-2]):
            return '股价持续在高位，向下穿透布林带中轨，建议卖出。'
        elif ((closing_prices[-10:] < ma5[-10:]).sum()>6) and (closing_prices[-1]>ma5[-1]) and (closing_prices[-2]<ma5[-2]):
            return '股价持续在低位，向上穿透布林带中轨，建议买入。'

        return '股价没有太大波动，建议持有。'

    def by_ma(self):
        return '均线理论建议结果。'
    
    def show(self):
        kdata = self.kdata.head(60)[::-1]
        dates = kdata.index
        highest_prices = kdata['high']
        lowest_prices = kdata['low']
        closing_prices = kdata['close']
        trend_points = (highest_prices + lowest_prices + closing_prices) / 3
        days = (pd.Series(dates) - pd.to_datetime('1970')).dt.days
        a = np.column_stack((days, np.ones_like(days)))
        x = np.linalg.lstsq(a, trend_points)[0]


header = ['date','open','high','low','close','volume','ma5','ma10','ma20']
kdata = pd.read_csv('k_data.csv', names=header, parse_dates=[0], index_col=0)
for i in range(100):
    model = StockPredictionModel(kdata[i:i+9][::-1])
    print(model.by_boll())