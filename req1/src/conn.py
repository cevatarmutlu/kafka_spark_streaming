import psycopg2
import src.config as config


def get_conn():
    postgres_cfg = config.get('postgres')
    conn = psycopg2.connect(**postgres_cfg)
    return conn
