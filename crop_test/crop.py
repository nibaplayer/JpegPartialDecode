import os
from PIL import Image


size_changed_path = "LED"
cropped_path = "LED"
imgl=os.listdir(cropped_path)
i,j=1,0

#改名
for img in imgl:
    image = Image.open(f"LED\\{img}")
    new_name = ""
    if img.endswith(".jpeg") and i<=9:
        # print(img)
        new_name = f"{i}_{j}.jpg"
        j=(j+1)%10
        if j==0:
            i+=1
        image.save(f"LED\\{new_name}")
    elif img.endswith(".jpeg") and i==10:
        j+=1
        new_name = f"test_{j}.jpg"
        image.save(f"LED\\{new_name}")