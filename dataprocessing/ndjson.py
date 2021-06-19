"""
    Bu script ndjson dosyası okur ve bir list' in içine ekler.
"""

import json

def get_data(path):
    """
        ndjson dosyalarını bir list' in içine ekler.

        Args:
            path: ndjson dosyasının yolu
        
        Return:
            (list): ndjson dosyasının içindeki veriler. 
    """
    ndjson = list()

    json_file = open(path, "r")
    
    for i in json_file:
        ndjson.append(
            json.loads(i)
        )
    
    return ndjson
