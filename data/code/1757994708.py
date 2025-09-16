import cv2
import numpy as np

# 创建一个白色背景的图像
img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# 绘制老虎的脸部基本形状（橙色背景）
cv2.ellipse(img, (250, 250), (200, 180), 0, 0, 360, (0, 100, 200), -1)

# 绘制眼睛（白色眼球）
cv2.circle(img, (200, 200), 40, (255, 255, 255), -1)
cv2.circle(img, (300, 200), 40, (255, 255, 255), -1)

# 绘制眼睛的眼球（黑色）
cv2.circle(img, (200, 200), 20, (0, 0, 0), -1)
cv2.circle(img, (300, 200), 20, (0, 0, 0), -1)

# 绘制鼻子
cv2.ellipse(img, (250, 250), (60, 40), 0, 0, 360, (0, 0, 0), -1)

# 绘制嘴巴（弯曲的线条）
cv2.ellipse(img, (250, 300), (80, 40), 0, 0, 180, (0, 0, 0), 3)

# 绘制舌头
points = np.array([[220, 320], [250, 340], [280, 320]], np.int32)
cv2.fillPoly(img, [points], (0, 0, 0))

# 绘制胸毛（老虎的胸前纹路）
cv2.line(img, (150, 150), (180, 180), (0, 0, 0), 3)
cv2.line(img, (350, 150), (320, 180), (0, 0, 0), 3)
cv2.line(img, (180, 120), (150, 100), (0, 0, 0), 3)
cv2.line(img, (320, 120), (350, 100), (0, 0, 0), 3)

# 显示图像
cv2.imshow('Tiger', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('tiger_drawing.png', img)
print("小老虎图像已保存为 'tiger_drawing.png'")