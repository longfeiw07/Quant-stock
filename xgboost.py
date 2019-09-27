from localStockInfo import localStockInfoInstance
import pandas as pd

if __name__ == '__main__':
  df = localStockInfoInstance.getStockDaily('002415.SZ')
