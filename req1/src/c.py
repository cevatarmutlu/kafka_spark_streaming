import pandas as pd
from pandas.core.frame import DataFrame
from datetime import datetime
import os
from src.utils import get_conn
from src.sql import c_query


def main():
   conn = get_conn()

   current_time = datetime.now()
   current_day = current_time.strftime("%Y-%d-%m")

   datas = pd.read_sql_query(c_query, conn)

   ta = os.path.exists(f"c_{current_day}.csv")
   if not ta:
      datas.to_csv(f"c_{current_day}.csv", index=False)
   else:
      exist_data = pd.read_csv(f"c_{current_day}.csv")
      exist_data[str(current_time.hour + 1)] = datas['d']
      exist_data.to_csv(f"c_{current_day}.csv", index=False)
