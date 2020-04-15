# -*- coding: utf-8 -*-
# @Time : 2020/4/14 下午4:13
# @Author : LuoLu
# @FileName: batch_remove_small.py
# @Software: PyCharm
# @Github ：https://github.com/luolugithub
# @E-mail ：argluolu@gmail.com

import glob
import os

import cv2 as cv
import numpy as np

root_path = '/home/luolu/PycharmProjects/ParticleDetection/'

if __name__ == '__main__':
    base_name = ''
    counter = 0
    for filename in glob.glob('data/yashi_qscan/mask/*.png'):
        img = cv.imread(filename, 0)
        # height, width, channels = img.shape
        print(filename)
        base_name = os.path.basename(filename)
        save_name = base_name.split('_')[0]

        # fill hole
        # read image, ensure binary
        img[img != 0] = 255

        # flood fill background to find inner holes
        holes = img.copy()
        cv.floodFill(holes, None, (0, 0), 255)

        # invert holes mask, bitwise or with img fill in holes
        holes = cv.bitwise_not(holes)
        filled_holes = cv.bitwise_or(img, holes)

        # remove_small_objects

        # find all your connected components (white blobs in your image)
        nb_components, output, stats, centroids = cv.connectedComponentsWithStats(filled_holes, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them,
        # such as size the following part is just taking out the background which is also considered a component,
        # but most of the time we don't want that.
        sizes = stats[1:, -1]
        nb_components = nb_components - 1

        # minimum size of particles we want to keep (number of pixels)
        # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
        min_size = 250

        # your answer image
        cleaned = np.zeros((output.shape))
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                cleaned[output == i + 1] = 255

        cv.imwrite(root_path + "data/yashi_qscan/cleaned/" + save_name + '.png', cleaned)
        counter = counter + 1

    print('counter: ', counter)