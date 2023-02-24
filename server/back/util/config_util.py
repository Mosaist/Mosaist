import os
import json

import util.json_util as json_util

CONFIG = json_util.DotDict(json.load(open(f'{os.path.dirname(__file__)}/../../../config.json')))