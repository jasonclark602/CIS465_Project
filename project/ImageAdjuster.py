# Image and other imports
import matplotlib
from PIL import ImageEnhance as Ime, Image as Img

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import math
from .constants import *


def open_img(path, errmsg):
    try:
        return Img.open(path, mode='r')
    except IOError as e:
        print(e)
        print(errmsg)


def _reset():
    img = open_img(PROJ_IMG_PATH, 'Reset Error')
    img.save(EDIT_IMG_PATH)
    img.close()


def _adjust_brightness(r, g, b):
    img = open_img(EDIT_IMG_PATH, 'failed to adjust rgb')

    red, green, blue = img.split()

    red = Ime.Brightness(red).enhance(r / 50)
    blue = Ime.Brightness(blue).enhance(b / 50)
    green = Ime.Brightness(green).enhance(g / 50)

    enhanced = Img.merge('RGB', (red, green, blue))
    enhanced.save(EDIT_IMG_PATH)

    enhanced.close()
    img.close()


def _base(is_gray):
    if is_gray:
        image = open_img(EDIT_IMG_PATH, 'failed at _base').convert('L')
        image.save(EDIT_IMG_PATH)
        image.close()
    else:
        _reset()


def _histogram():
    img = open_img(EDIT_IMG_PATH, 'failed to create histogram')

    if img.mode != 'L':
        red, green, blue = img.split()
        histogram, bin_edges = np.histogram(red, bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histogram, color='r')
        histogram, bin_edges = np.histogram(green, bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histogram, color='g')
        histogram, bin_edges = np.histogram(blue, bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histogram, color='b')
        plt.title('RGB Histogram')
        plt.xlabel('Color Value')
    else:
        histogram, bin_edges = np.histogram(img, bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histogram, color='k')
        plt.title('Gray Histogram')
        plt.xlabel('Intensity Value')

    plt.ylabel('Pixels')
    plt.savefig(HIST_IMG_PATH, format='jpg')

    plt.close()
    img.close()


def _entropy(probabilities):
    num = 0
    for x in probabilities:
        if x == 0:
            continue
        num += x * math.log2(x)

    num *= -1

    return num


def _difference_transformation():
    img = open_img(PROJ_IMG_PATH, 'failed at _diff').convert('L')
    img_copy = img.copy()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if x == 0:
                continue
            else:
                num1 = img.getpixel((x, y))
                num2 = img.getpixel((x - 1, y))
                result = (num1 - num2) % 256
                img_copy.putpixel((x, y), result)

    img_copy.save(EDIT_IMG_PATH)
    img_copy.close()
    img.close()


def _histogram2(img):
    histogram = np.zeros(256)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color = img.getpixel((i, j))
            num = color
            histogram[num] += 1

    return histogram


def entropy():
    gray_img = open_img(EDIT_IMG_PATH, 'failed at 105').convert('L')

    total_pixels = gray_img.size[0] * gray_img.size[1]

    # Histogram Calculation to Get probability
    probabilities = _histogram2(gray_img)

    # Adjust array to contain P(r) values by dividing each element by total_pixels
    for x in range(len(probabilities)):
        probabilities[x] = probabilities[x] / total_pixels

    gray_img.close()

    # Calculate the Entropy
    return _entropy(probabilities)
