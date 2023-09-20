import os
import sys
import time
from itertools import product
from multiprocessing import Process,Queue
import numpy as np

sys.path.append(f"JPG_Decoder")
from JPG_Decoder.jpg_decoder import JPGImage

fpath=f"datasets"
imgList=[]
imgl=os.listdir(fpath)

DCQueue=Queue()
ITQueue=Queue()
for img in imgl:
    if img.endswith(".jpg"):
        imgList.append(os.path.join(fpath,img))

def getDC(id,Q1,Q2):
    with open(imgList[id],"rb") as f:
        jpg=JPGImage(f)
        jpg.read_header()
        jpg.read_data()
        jpg.decode_huffman_data()
        with open("result.txt","a") as output:
            output.write(f"{id}\'sDC={jpg.DC}")
        return jpg.DC
        Q1.put(jpg.DC)
        Q2.put(jpg.DC_interval)

if __name__ == '__main__':

    p=Process(target=getDC,args=(4,DCQueue,ITQueue,))
    p.start()
    # p = Process(target=getDC, args=(5, DCQueue,ITQueue,))
    # p.start()
    # while DCQueue.qsize()<2 and ITQueue.qsize()<2:
    #     time.sleep(1)

    # dc1=DCQueue.get()
    # dc2=DCQueue.get()
    # it1=ITQueue.get()
    # it2=ITQueue.get()
    # Num,count,diff=len(dc1),0,[]
    # print(Num)
    # for d1,d2,i1,i2,i in zip(dc1,dc2,it1,it2,range(Num)):
    #     if i1==i2 and d1==d2:
    #         continue
    #     count+=1
    #     diff.append(i)
    #     print(i,d1-d2,d1,d2,i1,i2,i1-i2)
    # print(count,Num,float(count)/Num)

    # adc1=[abs(item) for item in dc1]
    # adc2 = [abs(item) for item in dc2]
    # print(min(adc1),min(adc2))
