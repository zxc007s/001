import cv2
import numpy as np

# 创建白色背景图像
img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# 绘制老虎头部（圆形）
cv2.circle(img, (250, 200), 100, (0, 165, 255), -1)

# 绘制耳朵（椭圆）
cv2.ellipse(img, (200, 120), (30, 40), 0, 0, 360, (0, 165, 255), -1)
cv2.ellipse(img, (300, 120), (30, 40), 0, 0, 360, (0, 165, 255), -1)

# 绘制眼睛
cv2.circle(img, (220, 180), 10, (0, 0, 0), -1)
cv2.circle(img, (280, 180), 10, (0, 0, 0), -1)

# 绘制鼻子
cv2.circle(img, (250, 220), 8, (0, 0, 0), -1)

# 绘制胡须
cv2.line(img, (230, 220), (200, 210), (0, 0, 0), 2)
cv2.line(img, (230, 230), (200, 240), (0, 0, 0), 2)
cv2.line(img, (270, 220), (300, 210), (0, 0, 0), 2)
cv2.line(img, (270, 230), (300, 240), (0, 0, 0), 2)

# 绘制胸前纹路
cv2.line(img, (200, 300), (300, 300), (0, 0, 0), 3)
cv2.line(img, (210, 320), (290, 320), (0, 0, 0), 3)
cv2.line(img, (220, 340), (280, 340), (0, 0, 0), 3)

# 添加文字标识
cv2.putText(img, 'Little Tiger', (180, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# 显示图像
cv2.imshow('Tiger Drawing', img)
cv2.waitKey(0)
cv2.destroyAllWindows()