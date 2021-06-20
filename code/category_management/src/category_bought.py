import pandas as pd
from datetime import datetime
from src.utils.sql import category_bought
from src.utils.conn import get_conn
import src.utils.config as config

def transform_datas(datas):
    grouped_datas = datas.groupby("categoryid")
    category_arr = datas['categoryid'].unique()

    category_prods = []
    for i in category_arr:
        category_prods.append(grouped_datas.get_group(i)['productid'].to_list())

    converted_datas = pd.DataFrame(category_prods, columns=[str(i) for i in range(1, 11)], index=list(map(lambda x: f"C-{x}", category_arr)))

    return converted_datas

def main():
    conn = get_conn()
    datas = pd.read_sql_query(category_bought, conn)

    transformed_datas = transform_datas(datas)

    now = datetime.now().strftime("%Y-%d-%m, %H")
    cfg = config.get('category_management')

    transformed_datas.to_csv(f"{cfg['output_path']}/category_bought_{now}.csv")
