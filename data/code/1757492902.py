import cv2
import numpy as np

# 创建白色背景图像
img = np.ones((500, 500, 3), dtype=np.uint8) * 255

# 绘制老虎身体（橙色圆形）
cv2.circle(img, (250, 250), 150, (0, 165, 255), -1)

# 绘制耳朵（两个小圆形）
cv2.circle(img, (200, 150), 40, (0, 165, 255), -1)
cv2.circle(img, (300, 150), 40, (0, 165, 255), -1)

# 绘制眼睛（两个黑色圆形）
cv2.circle(img, (200, 220), 20, (0, 0, 0), -1)
cv2.circle(img, (300, 220), 20, (0, 0, 0), -1)

# 绘制鼻子（红色圆形）
cv2.circle(img, (250, 280), 15, (0, 0, 255), -1)

# 绘制肠子（白色圆形）
cv2.circle(img, (250, 350), 60, (255, 255, 255), -1)

# 绘制肠纹（黑色线条）
cv2.line(img, (220, 320), (280, 320), (0, 0, 0), 2)
cv2.line(img, (210, 340), (290, 340), (0, 0, 0), 2)
cv2.line(img, (220, 360), (280, 360), (0, 0, 0), 2)

# 绘制尾巴（曲线）
points = np.array([[350, 250], [400, 200], [450, 250], [400, 300]], np.int32)
points = points.reshape((-1, 1, 2))
cv2.polylines(img, [points], False, (0, 165, 255), 5)

# 显示图像
cv2.imshow('Tiger', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存图像
cv2.imwrite('tiger.png', img)

print("小老虎图像已绘制完成并保存为 'tiger.png'")