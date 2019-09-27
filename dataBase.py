import pymysql
import json
import traceback,sys

class dataBase():
  db_init = {}

  def __init__(self):
    with open('config.json', 'r') as f:
      cfg = json.load(f)
    db_cfg = cfg['dataBase']
    db = db_cfg['db']
    for db_name in db:
      self.db_init[db_name] = pymysql.connect(host=db_cfg['host'], user=db_cfg['user'],
                                              passwd=db_cfg['passwd'], db=db_name, port=db_cfg['port'],
                                              unix_socket=db_cfg["unix_socket"], charset='utf8')

  def connectToTable(self, table_name):
    return self.db_init[table_name]

  def showAllTables(self):
    db_name = self.db_init.keys()
    print(db_name)

  # args 用元组给出SQL中需要填充的数据
  def select(self, table_name, sql, args=None):
    if self.db_init.get(table_name) == None:
      return ((None,))
    stock_table = dataBaseInstance.connectToTable(table_name)
    cursor = stock_table.cursor()
    cursor.execute(sql, args)
    data = cursor.fetchall()
    cursor.close()
    return data

  def insert(self, table_name, sql, args):
    if self.db_init.get(table_name) == None:
      return False
    try:
      stock_table = dataBaseInstance.connectToTable(table_name)
      cursor = stock_table.cursor()
      cursor.execute(sql, args)
      stock_table.commit()
      cursor.close()
      return True
    except :
      print('stock table:{} insert异常, sql:{}, args:{}'.format(table_name, sql, args))
      stock_table.rollback()
      cursor.close()
      traceback.print_exc(file=sys.stdout)
      return False

dataBaseInstance = dataBase()

# args=(str('2019-09-25'), str('002415.SZ'), float(33.88), float(33.06), float(33.92), float(33.0), float(364871.79), float(1214562.271), float(34.09), float(-1.03), float(-3.0214))
# sql_insert = "INSERT IGNORE INTO stock_daily(state_dt,stock_code,open,close,high,low,vol,amount,pre_close,amt_change,pct_change) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"
# dataBaseInstance.insert('stock',sql_insert,args)