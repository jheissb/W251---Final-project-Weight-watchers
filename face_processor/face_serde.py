import numpy as np
import json
from collections import namedtuple


class FaceEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
   
def faceDecoder(faceImgDict):
    return namedtuple('FacceImage', faceImgDict.keys())(*faceImgDict.values())