import datetime
import tushare as ts
import json
from dataBase import dataBaseInstance
import sys,traceback

class GetDataFromTushare:
  stock_pool = []
  tushare_cfg = {}
  pro = ts.pro_api()

  def __init__(self):
    # 设置tushare
    with open('config.json') as f:
      cfg = json.load(f)
    self.tushare_cfg = cfg['tushare']
    ts.set_token(self.tushare_cfg['token'])
    self.stock_pool = self.tushare_cfg['stock_pool']
    print('stock pool {} init succ~'.format(self.stock_pool))

  def getStockPool(self):
    return self.stock_pool

  # 插入stock_code的日线  数据
  def InsertStockDaily(self, stock_code, start_time, end_time):
    try:
      # tushare读取stock_code的日线数据
      df = self.pro.daily(ts_code=stock_code, start_date=start_time, end_date=end_time)
      # 写入数据库
      c_len = df.shape[0]
      for j in range(c_len):
        resu0 = list(df.ix[c_len - 1 - j])
        resu = []
        for k in range(len(resu0)):
          if str(resu0[k]) == 'nan':
            resu.append(-1)
          else:
            resu.append(resu0[k])
        state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
        args = (state_dt, str(resu[0]), float(resu[2]), float(resu[5]), float(resu[3]), float(resu[4]), float(resu[9]),
                float(resu[10]), float(resu[6]), float(resu[7]), float(resu[8]))
        sql_insert = "INSERT IGNORE INTO stock_daily(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
        dataBaseInstance.insert('stock', sql_insert, args)
      print('stack_code:{} update from {} to {}'.format(stock_code, start_time, end_time))
    except :
      print('No DATA Code: ' + stock_code)
      traceback.print_exc(file=sys.stdout)
      return

  def updateStockList(self):
    try:
      args = 'ts_code,symbol,name,area,industry,market,list_date'
      df = self.pro.stock_basic(exchange='', list_status='L', fields=args)
      row_num = df.shape[0]
      for i in range(row_num):
        row = list(df.ix[row_num - 1 - i])
        sql_replace = "REPLACE INTO stock_list(stock_code,symbol,name,area,industry,market,list_date) VALUES(%s, %s, %s, %s,%s,%s,%s)"
        dataBaseInstance.insert('stock', sql_replace, row)
      print('Time:{}, update stock List to lastest~'.format(datetime.datetime.now()))
    except :
      print('update Stock List fail~')
      traceback.print_exc(file=sys.stdout)
      return


tushareInstance = GetDataFromTushare()


# 读取stock库中的相关状态
class StockState:
  stock_table = 'stock'

  # 获取上市日期
  def getListDate(self, stock_code):
    sql = "SELECT list_date FROM stock.stock_list WHERE stock_code=%s"
    args = (stock_code)
    list_dt = dataBaseInstance.select(self.stock_table, sql, args)
    if list_dt[0][0] == None:
      return 0
    return list_dt[0][0]

  # 某支股票本地最新数据的日期
  def getStockLastLocalDate(self, stock_code):
    sql = "SELECT max(state_dt) FROM stock.stock_daily WHERE stock_code=%s"
    args = (stock_code)
    last_state_dt = dataBaseInstance.select(self.stock_table, sql, args)
    if last_state_dt[0][0] == None:
      return 0
    return last_state_dt[0][0]


stockStateInstance = StockState()

if __name__ == '__main__':
  # 更新股票列表
  # tushareInstance.updateStockList()
  # 更新stock_pool至昨天
  time_temp = datetime.datetime.now()
  end_dt = time_temp.strftime('%Y%m%d')
  for stock_code in tushareInstance.getStockPool():
    start_dt = stockStateInstance.getStockLastLocalDate(stock_code)
    if start_dt == 0:
      start_dt = stockStateInstance.getListDate(stock_code)
    else:
      start_dt += datetime.timedelta(days=1)
    start_dt = start_dt.strftime('%Y%m%d')
    tushareInstance.InsertStockDaily(stock_code, start_dt, end_dt)
