from numpy import index_exp
import pandas as pd
from datetime import datetime
import os
from src.utils.conn import get_conn
from src.utils.sql import conversion_rates
import src.utils.config as config

def writeToCSV(datas):
   cfg = config.get('category_management')

   current_time = datetime.now()
   current_day = current_time.strftime("%Y-%d-%m")
   csv_path = f"{cfg['output_path']}/conversion_rates_{current_day}.csv"

   if not os.path.exists(csv_path):
      datas = datas.rename(columns={'0': current_time.hour})
      datas.to_csv(csv_path, index=False)
   else:
      exist_data = pd.read_csv(csv_path)
      exist_data[str(current_time.hour + 1)] = datas['0']
      exist_data.to_csv(csv_path, index=False)

def main():
   conn = get_conn()

   datas = pd.read_sql_query(conversion_rates, conn)

   writeToCSV(datas)

   
