import cv2
import numpy as np
import os




def cropped_circle(file,o,c):
    # 读取图像
    image = cv2.imread(f"{o}\\{file}", cv2.IMREAD_COLOR)

    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 高斯模糊
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 检测圆
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=200, param2=30, minRadius=0, maxRadius=0)

    # 裁剪目标圆的矩形区域
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # 计算矩形区域的左上角和右下角坐标
            x1 = x - r
            y1 = y - r
            x2 = x + r
            y2 = y + r
            # 裁剪出目标圆的矩形区域
            cropped = image[y1:y2, x1:x2]
            # 显示裁剪后的图像
            # cv2.imshow("Cropped Circle", cropped)
            cv2.imwrite(f"{c}\\{file}", cropped)
            break
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

original_path = "original"
cropped_path = "cropped"
imgList = []
imgl=os.listdir(original_path)
for img in imgl:
    if img.endswith(".jpg"):
        imgList.append(img)
        cropped_circle(img,original_path,cropped_path)


