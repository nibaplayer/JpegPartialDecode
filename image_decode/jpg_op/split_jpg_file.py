import os


def getHead(data,i):
    return (data[i] << 8) | data[i+1]

def parse_quantization_table(segment_data):
    # 从段数据中解析亮度分量或色度分量的量化表
    table = [0] * 64
    table_id = segment_data[0]  # 亮度分量表编号为 0，色度分量表编号为 1

    for i in range(64):
        table[i] = segment_data[i + 1]

    return table_id, table

def parse_frame_header(segment_data):
    # 解析帧头段的数据
    precision = segment_data[0]
    height = (segment_data[1] << 8) + segment_data[2]
    width = (segment_data[3] << 8) + segment_data[4]
    num_components = segment_data[5]

    components = []

    for i in range(num_components):
        component_id = segment_data[6 + i * 3]
        sampling_factors = segment_data[7 + i * 3]
        quantization_table_id = segment_data[8 + i * 3]

        component = {
            "id": component_id,
            "sampling_factors": (sampling_factors >> 4, sampling_factors & 0x0F),
            "quantization_table_id": quantization_table_id
        }

        components.append(component)

    return {
        "precision": precision,
        "height": height,
        "width": width,
        "num_components": num_components,
        "components": components
    }




fpath=f'D:\paper\Evs_Scheduler\image_diff\image'
image_path=os.path.join(fpath,"1_1.jpg")

with open(image_path, 'rb') as file:
    # 读取文件内容
    data = file.read()



# APPN OP
i=2
APPn=range(0xffe0,0xfff0)
while getHead(data,i) in APPn:
    length=getHead(data,i+2)
    i+=2+length

# 量化表

if getHead(data,i)==0xffdb:
    length=getHead(data,i+2)
    i+=4

seg=data[i:i+length]
print(parse_quantization_table(seg))
i+=length-2

# 帧头
if getHead(data,i)==0xffdb:
    length=getHead(data,i+2)
    i+=4
seg=data[i:i+length]
print(parse_quantization_table(seg))
i+=length-2



if getHead(data,i)==0xffc0:
    length=getHead(data,i+2)
    i+=4
seg=data[i:i+length]
print(parse_frame_header(seg))
i+=length-2

while getHead(data,i)==0xffc4:
    length=getHead(data,i+2)
    id=data[i+4]
    i+=5
    code_lengths=data[i:i+16]
    code_values=data[i+16:i+length-3]
    i+=length-3
    print(length,hex(id),list(code_lengths),list(code_values))

if getHead(data,i)==0xffda:
    length = getHead(data, i + 2)
    num_components=data[i+4]
    i+=5
    print(length, num_components)
    for _ in range(num_components):
        component_descriptor=data[i:i+2]
        component_id = component_descriptor[0]
        # 高 4 位是采样因子，低 4 位是哈夫曼表索引
        horizontal_sampling_factor = (component_descriptor[1] >> 4) & 0xFF
        vertical_sampling_factor = component_descriptor[1] & 0xFF
        print(component_id,horizontal_sampling_factor,vertical_sampling_factor)
        i+=2
    print(getHead(data,i),data[i+2])
i+=3
while getHead(data,i)!=0xffda and i <len(data)-2:
    i+=1
print(hex(getHead(data,i)))
# # 遍历每个比特
# for byte in data:
#     # 处理每个比特，例如打印它们的十六进制表示
#     print(hex(byte))
# 打开 JPEG 文件以二进制读取模式打开
# with open(image_path, 'rb') as f:
#     data = f.read()
#
# # 初始化一个字典用于存储不同段的数据
# jpeg_data = {}
#
# # 定义起始标志位和对应的描述
# markers = {
#     0xFFD8: "SOI",
#     0xFFE0: "APPn",
#     0xFFDB: "Quantization Tables",
#     0xFFC0: "Frame Header",
#     0xFFDA: "Scan Header",
#     0xFFC4: "Huffman Tables",
#     0xFFD9: "EOI"
# }
#
# # 循环遍历 JPEG 数据，查找各个段
# i = 0
# while i < len(data):
#     # 读取两个字节作为标志位
#     marker = (data[i] << 8) | data[i + 1]
#
#     # 查找标志位是否在markers字典中
#     if marker in markers:
#         # 如果是，找到段的起始位置和结束位置
#         segment_start = i
#         i+=2
#         while i < len(data) and marker not in markers:  # 直到遇到EOI（结束标志位）
#             i += 1
#             marker = (data[i] << 8) | data[i + 1]
#         segment_end = i   # 包括结束标志位
#         segment_data = data[segment_start:segment_end]
#         # 存储段的数据
#         jpeg_data[markers[marker]] = segment_data
#
#     # i += 2  # 移动到下一个标志位
#
# # 输出字典
# for key, value in jpeg_data.items():
#     print(key, ":", value)
# print(jpeg_data.keys())