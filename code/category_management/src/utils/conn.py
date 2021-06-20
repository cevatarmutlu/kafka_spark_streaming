import psycopg2
import src.utils.config as config


def get_conn():
    postgres_cfg = config.get('postgres')
    
    conn = psycopg2.connect(
        host=postgres_cfg['host'],
        database=postgres_cfg['database'],
        user=postgres_cfg['user'],
        password=postgres_cfg['password']
    )
    return conn
