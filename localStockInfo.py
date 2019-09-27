from dataBase import dataBaseInstance
import pandas as pd

# 查询本地数据库常用股票数据
class localStockInfo:
  # param stock_code
  # return df
  def getStockDaily(self, stock_code):
    # 获取字段名
    sql_stock_info = "DESC stock_daily"
    data = dataBaseInstance.select('stock', sql_stock_info)
    row_num = len(data)
    col_name = []
    for i in range(row_num):
      col_name.append(data[i][0])
    # 获取数据
    args = (stock_code,)
    sql_stock_daily = "SELECT * FROM stock_daily WHERE stock_code=%s"
    data = dataBaseInstance.select('stock', sql_stock_daily, args)
    dic = {k: [] for k in col_name}
    for i in range(len(data)):
      for j in range(len(col_name)):
        dic[col_name[j]].append(data[i][j])
    df=pd.DataFrame(dic,columns=col_name)
    return df


localStockInfoInstance = localStockInfo()

if __name__ == '__main__':
  # test_getStockDaily
  df=localStockInfoInstance.getStockDaily("002415.SZ")
  print('columns:{}'.format(df.columns))
  print('indexs num:{}'.format(df.index))
  print(df.head(5))
