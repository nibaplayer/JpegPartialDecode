import os
import sys
import numpy as np

sys.path.append(f"JPG_Decoder")
from JPG_Decoder.jpg_decoder import JPGImage


import pickle
import base64
import zlib


def pack(v):
    return zlib.compress(base64.b64encode(pickle.dumps(v)))

def unpack(v):
    return pickle.loads(base64.b64decode(zlib.decompress(v)))

fpath="cropped"
imgl=os.listdir(fpath)
# out_path="DCresults"

def getDC(file):
    with open(file,"rb") as f:
        jpg=JPGImage(f)
        jpg.read_header()
        jpg.read_data()
        jpg.decode_huffman_data()
        return jpg.DC
result={}
for img in imgl:
    if img.endswith(".jpg") and "Green" in img:
        dc=getDC(os.path.join(fpath,img))
        result[img]=dc
        print(img)

with open("Button_results","wb") as f:
    f.write(pack(result))

