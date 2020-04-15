# -*- coding: utf-8 -*-
# @Time : 2020/3/23 下午4:30
# @Author : LuoLu
# @FileName: count_mask.py
# @Software: PyCharm
# @Github ：https://github.com/luolugithub
# @E-mail ：argluolu@gmail.com
import cv2
import matplotlib
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL.Image import Image

matplotlib.use('TkAgg')
cv.namedWindow("original", flags=2)
cv.namedWindow("binary", flags=2)
cv.namedWindow("colored labels", flags=2)

path = "/home/luolu/PycharmProjects/ParticleDetection/data/yashi_qscan/edge/edge_cl.png"
# img_src = "/home/luolu/PycharmProjects/ParticleDetection/data/yashi_qscan/binary_test.png"
original = cv.imread(path)
# src_image = cv.imread(img_src)
height, width, channels = original.shape
src = cv.GaussianBlur(original, (3, 3), 0)
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
ret, binary_ = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)

# 使用开运算去掉外部的噪声
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
binary = cv.morphologyEx(binary_, cv.MORPH_OPEN, kernel)
# gray_correct = np.array(255 * (gray / 255) ** 1.2, dtype='uint8')
# thresh = cv.adaptiveThreshold(gray_correct, 50, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 255, 50)
# binary = cv.bitwise_not(thresh)
cv.imshow("original", original)
cv.imshow("binary", binary_)
# cv.imshow("binary digit", binary_)

num_labels, labels, stats, centers = cv.connectedComponentsWithStats(binary, connectivity=4, ltype=cv.CV_32S)
colors = []
for i in range(num_labels):
    b = np.random.randint(0, 256)
    g = np.random.randint(0, 256)
    r = np.random.randint(0, 256)
    colors.append((b, g, r))

# add continuous pixel count
img = cv2.imread(path, 0)
img = cv2.GaussianBlur(img, (1, 1), 0)
img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
num_labels_original, labels_im = cv2.connectedComponents(img)
count = [0] * (num_labels_original)
# print("count len:", range(1, num_labels_original, 1))
# for num in range(num_labels_original):
#     for i in range((labels_im == num).shape[0]):
#         for j in range((labels_im == num).shape[1]):
#             if (labels_im == num)[i][j] == 1:
#                 count[num] = count[num] + 1
#
# dots = 0
# line = 0
# for iterm in range(1, len(count), 1):
#     # print("iterm" + str(iterm) + ":", count[iterm])
#     if count[iterm] > 10:
#         line = line + 1
#     else:
#         dots = dots + 1

colors[0] = (0, 0, 0)
image = np.copy(src)
for t in range(1, num_labels, 1):
    x, y, w, h, area = stats[t]
    cx, cy = centers[t]
    # 标出中心位置
    # cv.circle(src_image, (np.int32(cx), np.int32(cy)), 1, (255, 0, 0), 0, 1, 0)
    # 画出外接矩形
    cv.rectangle(image, (x, y), (x + w, y + h), colors[t], 1, 8, 0)
    # cv.putText(src_image, str(t).__add__(":L=").__add__(str(count[t])), (x, y), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1)
    cv.putText(image, str(t), (x, y), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 1)
    print("label index %d, area of the label : %d" % (t, area))

    cv.imshow("colored labels", image)
    # cv.imwrite("labels.png", image)
    print("total number : ", num_labels - 1)
    cv.putText(image, "contact Sum:" + str(num_labels - 1), (30, 960), cv.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 3)
    # cv.putText(src_image, "dots:" + str(dots), (30, 300), cv.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)
    # cv.putText(src_image, "lines:" + str(line), (30, 330), cv.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 255), 2)

# input = cv.imread("granule.png")
# connected_components_stats_demo(input)
cv.waitKey(0)
cv.destroyAllWindows()
