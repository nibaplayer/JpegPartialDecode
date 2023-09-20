import os
import random
import sys
import time
from itertools import product
from multiprocessing import Process,Queue
import numpy as np

sys.path.append(f"D:\project\JpegPartialDecode\JPG_Decoder")
from JPG_Decoder.jpg_decoder import JPGImage

fpath=f"D:\project\JpegPartialDecode\datasets"
imgList=[]
imgl=os.listdir(fpath)
for img in imgl:
    if img.endswith(".jpg"):
        imgList.append(os.path.join(fpath,img))
IMGQueue=Queue()

def HuffDecodeImg(id,Q):
    with open(imgList[id],"rb") as f:
        jpg=JPGImage(f)
        jpg.read_header()
        jpg.read_data()
        jpg.decode_huffman_data()
        Q.put((id,jpg.mcus,jpg.DC,jpg.DC_interval))

def getJPG(id):
    with open(imgList[id],"rb") as f:
        jpg=JPGImage(f)
        jpg.read_header()
    return jpg

def SolveComponent(jpg):
    for component_id, component in jpg.color_components.items():
        if component_id == 1:
            assert component.horizontal_sampling_factor in (1, 2) and component.vertical_sampling_factor in (1, 2)
            jpg.horizontal_sampling_factor = component.horizontal_sampling_factor
            jpg.vertical_sampling_factor = component.vertical_sampling_factor
        else:
            assert component.horizontal_sampling_factor == 1 and component.vertical_sampling_factor == 1

    # 根据sampling判断mcu的总大小
    mcu_width = (jpg.width + 7) // 8
    mcu_height = (jpg.height + 7) // 8  # 8是最小单位，图片宽度不够要补全
    if jpg.horizontal_sampling_factor == 2 and mcu_width % 2 == 1:  # 如果sampling==2的话，就必须是偶数个，因为是2个2个编解码的
        mcu_width += 1
    if jpg.vertical_sampling_factor == 2 and mcu_height % 2 == 1:
        mcu_height += 1
    return mcu_width,mcu_height,jpg.components_num,jpg.vertical_sampling_factor,jpg.horizontal_sampling_factor

if __name__ == '__main__':
    id1,id2,change_probability=2,5,0.5
    p1=Process(target=HuffDecodeImg,args=(id1,IMGQueue,))
    p1.start()
    p2 = Process(target=HuffDecodeImg, args=(id2,IMGQueue,))
    p2.start()
    while IMGQueue.qsize()<2 :
        time.sleep(1)
    k1,m1,dc1,di1=IMGQueue.get()
    k2,m2,dc2,di2=IMGQueue.get()
    mcus,dcs={},{}
    mcus[k1],dcs[k1]=m1,dc1
    mcus[k2],dcs[k2]=m2,dc2
    jpg1,jpg2=getJPG(id1),getJPG(id2)
    jpg1.mcus,jpg2.mcus=mcus[id1],mcus[id2]
    w1,h1,c1,vf1,hf1=SolveComponent(jpg1)
    w2, h2, c2,vf2,hf2 = SolveComponent(jpg2)
    pt1,pt,count=0,0,0
    if not (w1==w2 and h1==h2 and c1 ==c2 and vf1 ==vf2 and hf1 ==hf2):
        exit(0)
    for d1,d2 in zip(dc1,dc2):
        if abs(d1 - d2) < 20:
            count+=1
    print(f"sim:{count},w:{w1},h:{h1},hf:{hf1},vf:{vf1}")
    for i, j in product(range(0, h1, vf1),range(0, w1, hf1)):
        for voff, hoff in product(range(vf1), range(hf1)):
            pt1+=1
            if pt1 < len(dc1):
                if abs(dc1[pt1]-dc2[pt1])<20 :#and random.random()<change_probability:
                    jpg1.mcus[i + voff, j + hoff, 0] = jpg2.mcus[i + voff, j + hoff, 0]
                    pt+=1
        for k in range(1, c1):
            pt1 += 1
            if pt1<len(dc1):
                if abs(dc1[pt1] - dc2[pt1]) < 20:# and random.random() < change_probability:
                    pt += 1
                    for voff, hoff in product(range(vf1), range(hf1)):
                        jpg1.mcus[i + voff, j + hoff, k] = jpg2.mcus[i, j, k]

    jpg1.dequantize_mcu()
    jpg1.inverse_DCT()
    jpg1.color_convertion()
    jpg1.save(id1)
    print(pt)
    print(pt1)



