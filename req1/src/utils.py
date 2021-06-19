import psycopg2
import yaml

def __load_yaml__():
    return yaml.safe_load(open("src/config.yml"))

def get(name):
    yaml_file = __load_yaml__()
    return yaml_file[name]

def get_conn():
    postgres_cfg = get('postgres')
    conn = psycopg2.connect(**postgres_cfg)
    return conn
