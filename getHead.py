import os
import sys

import numpy as np

sys.path.append(f"D:\project\JpegPartialDecode\JPG_Decoder")
from JPG_Decoder.jpg_decoder import JPGImage

fpath=f"D:\project\JpegPartialDecode\datasets"
imgList=[]
imgl=os.listdir(fpath)
for img in imgl:
    if img.endswith(".jpg"):
        imgList.append(os.path.join(fpath,img))


def getHead(id,imgList=imgList):
    with open(imgList[id],"rb") as f:
        jpg=JPGImage(f)
        jpg.read_header()
        return jpg.huffman_tables_DC,jpg.huffman_tables_DC,jpg.quantization_tables

dcl,acl,ql=[],[],[]
Num=len(imgList)
for i in range(Num):
    dc,ac,q=getHead(i)
    dcl.append(dc)
    acl.append(ac)
    ql.append(q)


print("-------------------------------------------")

for i in range(11):
    if not (acl[0]==acl[i]):
        print(i)
    if not (dcl[0]==dcl[i]):
        print(i)
    if not all(np.array_equal(ql[0][key], ql[i][key]) for key in ql[0].keys()):
        print(i)





