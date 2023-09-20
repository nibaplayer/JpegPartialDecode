from PIL import Image
import os 


def resize(file,input_d,output_d,target_width,target_height):
    image = Image.open(f"{input_d}\\{file}")
    resized_image = image.resize((target_width,target_height))
    resized_image.save(f"{output_d}\\{file}")


size_changed_path = "SizeChanged"
cropped_path = "cropped"
imgl=os.listdir(cropped_path)
for img in imgl:
    if img.endswith(".jpg"):
        resize(img,cropped_path,size_changed_path,120,120)
