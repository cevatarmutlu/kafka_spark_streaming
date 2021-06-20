"""
    Bu script config.yml dosyasındaki verileri okumaya yarar.
"""

import yaml

def __load_yaml__() -> dict:
    """
        config.yml dosyasını yaml formatında load eder.

        Return:
            dict: yml dosyasının tamamı.
    """
    return yaml.safe_load(open("../../config.yml"))

def get(name: str) -> dict:
    """
        Parametre olarak verilen değeri config dosyasından getirir.

        Args:
            name(str): config dosyasından okunacak değer.
        
        Return:
            dict: yaml dosyasındaki değer.
    """

    yaml_file = __load_yaml__()

    return yaml_file[name]
