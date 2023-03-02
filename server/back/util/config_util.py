import os
import json

class DotDict(dict):
    def __getattr__(*args):
        val = dict.get(*args)
        return DotDict(val) if type(val) is dict else val

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

CONFIG = DotDict(json.load(open(f'{os.path.dirname(__file__)}/../../../config.json')))