import cv2
import numpy as np

# 创建白色背景画布
canvas = np.ones((500, 500, 3), dtype=np.uint8) * 255

# 绘制身体（黄色椭圆）
cv2.ellipse(canvas, (250, 300), (100, 60), 0, 0, 360, (0, 165, 255), -1)

# 绘制头部（黄色圆形）
cv2.circle(canvas, (250, 200), 70, (0, 165, 255), -1)

# 绘制耳朵（两个棕色椭圆）
cv2.ellipse(canvas, (200, 150), (30, 20), 30, 0, 360, (0, 75, 150), -1)
cv2.ellipse(canvas, (300, 150), (30, 20), 330, 0, 360, (0, 75, 150), -1)

# 绘制眼睛（两个黑色圆形）
cv2.circle(canvas, (220, 190), 10, (0, 0, 0), -1)
cv2.circle(canvas, (280, 190), 10, (0, 0, 0), -1)

# 绘制鼻子（棕色三角形）
pts = np.array([[250, 210], [240, 230], [260, 230]], np.int32)
cv2.fillPoly(canvas, [pts], (0, 75, 150))

# 绘制嘴巴（黑色线条）
cv2.line(canvas, (240, 240), (260, 240), (0, 0, 0), 2)

# 绘制胡项（多条黑色线条）
cv2.line(canvas, (240, 230), (220, 225), (0, 0, 0), 1)
cv2.line(canvas, (240, 235), (215, 235), (0, 0, 0), 1)
cv2.line(canvas, (240, 240), (220, 245), (0, 0, 0), 1)
cv2.line(canvas, (260, 230), (280, 225), (0, 0, 0), 1)
cv2.line(canvas, (260, 235), (285, 235), (0, 0, 0), 1)
cv2.line(canvas, (260, 240), (280, 245), (0, 0, 0), 1)

# 绘制纹条（多条棕色线条）
cv2.line(canvas, (250, 250), (250, 350), (0, 75, 150), 3)
cv2.line(canvas, (220, 260), (230, 350), (0, 75, 150), 2)
cv2.line(canvas, (280, 260), (270, 350), (0, 75, 150), 2)

# 显示图像
cv2.imshow('Little Tiger', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()