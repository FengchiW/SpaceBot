import json
from typing import Dict

def as_dict(file) -> Dict:
    # if the file is given as a filename
    if isinstance(file, str):
        file = open(file)
    return json.load(file)


def get_values(file, *args) -> Dict:
    values = dict()
    file_dict = as_dict(file)
    for s in args:

    pass