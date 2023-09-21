from PIL import Image
import os 


def resize(file,new_name,input_d,output_d,target_width,target_height):
    image = Image.open(f"{input_d}\\{file}")
    # crop_area = (756+100-20, 756-50-20, 756*3+100-200-20, 756*3-50-200-20)
    # cropped_image = image.crop(crop_area)
    resized_image = image.resize((target_width,target_height))
    # file.replace("IMG_","")
    # file.replace(".jpeg","")
    # new_file = f"{i}_{j}.jpg"
    resized_image.save(f"{output_d}\\{new_name}")


size_changed_path = "buttons"
cropped_path = "buttons"
# imgl=os.listdir(cropped_path)
# i,j=1,0
# for img in imgl:
#     if img.endswith(".jpg") and i<=9:
#         # print(img)
#         new_name = f"{i}_{j}.jpg"
#         resize(img,new_name,cropped_path,size_changed_path,120,120)
#         j=(j+1)%10
#         if j==0:
#             i+=1
#     elif img.endswith(".jpeg") and i==10:
#         new_name = f"test_{j+1}"
#         resize(img,new_name,cropped_path,size_changed_path,120,120)
#         j+=1

resize("GreenOff_0.jpg","test_0.jpg",size_changed_path,size_changed_path,120,120)
