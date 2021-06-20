import yaml

def __load_yaml__():
    return yaml.safe_load(open("dataprocessing/config.yml"))

def get(name):
    yaml_file = __load_yaml__()
    return yaml_file[name]