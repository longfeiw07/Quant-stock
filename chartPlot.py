import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib import ticker as mticker
from mpl_finance import candlestick_ohlc
import datetime as dt
from localStockInfo import localStockInfoInstance
import numpy as np


def readStockData(stockCode, start_dt, end_dt):
  df = localStockInfoInstance.getStockDaily(stockCode)
  df = df[(df['state_dt'] > start_dt) & (df['state_dt'] <= end_dt)].reset_index(drop=True)
  return df


def simpleMovingAverage(list, MA):
  if len(list) < MA:
    return
  sma = list.copy()
  index = MA - 1
  while index < len(list):
    sma[index] = np.mean(list[index - MA + 1:index + 1])
    index += 1
  return sma


if __name__ == "__main__":

  #控制参数
  stock_code = '000988.SZ'
  MA1 = 10
  MA2 = 50
  startdate = dt.date(2019, 5, 1)
  enddate = dt.date(2019, 10, 9)

  # 读取数据
  days = readStockData(stock_code, startdate, enddate)
  daysreshape = days[['state_dt', 'open', 'high', 'low', 'close']]
  daysreshape.columns = ['DateTime', 'Open', 'High', 'Low', 'Close']
  daysreshape['DateTime'] = mdates.date2num(daysreshape['DateTime'])

  SP = MA2 - 1
  # K线图
  fig = plt.figure(facecolor='black', figsize=(15, 10))
  ax1 = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)
  ax1.patch.set_facecolor('black')
  candlestick_ohlc(ax1, daysreshape.values[SP:], width=.6, colorup='#ff1717', colordown='#53c156')
  ax1.grid(True, color='w')
  ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
  ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
  ax1.spines['bottom'].set_color("#5998ff")
  ax1.spines['top'].set_color("#5998ff")
  ax1.spines['left'].set_color("#5998ff")
  ax1.spines['right'].set_color("#5998ff")
  ax1.tick_params(axis='y', colors='w')
  plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
  ax1.tick_params(axis='x', colors='w')
  ax1.yaxis.label.set_color("w")
  plt.ylabel('Stock price and Volume')

  # 简单平滑移动曲线
  Av1 = simpleMovingAverage(daysreshape.Close.values, MA1)
  Av2 = simpleMovingAverage(daysreshape.Close.values, MA2)
  Label1 = str(MA1) + ' SMA'
  Label2 = str(MA2) + ' SMA'
  ax1.plot(daysreshape.DateTime.values[SP:], Av1[SP:], 'white', label=Label1, linewidth=1.5)
  ax1.plot(daysreshape.DateTime.values[SP:], Av2[SP:], '#4ee6fd', label=Label2, linewidth=1.5)

  plt.show()
