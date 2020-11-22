# Image and other imports
from PIL import Image as Img
from django.conf import settings
from matplotlib import pyplot as plt
import numpy as np
import os


import math

EDIT_IMG_PATH = './media/images/edit.jpg'


def _adjust_rgb():
    return 0


def _base(is_gray):
    if is_gray:
        image = Img.open(EDIT_IMG_PATH).convert('L')
        image.save(EDIT_IMG_PATH)
        image.close()


def _histogram(img):
    red, green, blue = img.split()
    histogram, bin_edges = np.histogram(red, bins=256, range=(0, 256))
    plt.plot(bin_edges[0:-1], histogram, color='r')
    histogram, bin_edges = np.histogram(green, bins=256, range=(0, 256))
    plt.plot(bin_edges[0:-1], histogram, color='g')
    histogram, bin_edges = np.histogram(blue, bins=256, range=(0, 256))
    plt.plot(bin_edges[0:-1], histogram, color='b')
    plt.title('RGB Histogram')
    plt.xlabel('Color Value')
    plt.ylabel('Pixels')
    return plt



def _entropy(probabilities):
    num = 0
    for x in probabilities:
        if x == 0:
            continue
        num += x * math.log2(x)

    num *= -1

    return num


def _difference_transformation(img):
    img_copy = img.convert("L")

    for x in range(img_copy.size[0]):
        for y in range(img_copy.size[1]):
            if x == 0:
                continue
            else:
                num1 = img_copy.getpixel((x, y))
                num2 = img_copy.getpixel((x - 1, y))
                result = (num1 - num2) % 256
                img.putpixel((x, y), result)
    return img


def calculations():
    try:
        img = Img.open(EDIT_IMG_PATH)
    except IOError:
        print('Cannot open edit image.')
        return 0

    entropy = 0
    entropy2 = 0

    gray_img = img.convert("L")

    total_pixels = gray_img.size[0] * gray_img.size[1]

    # Histogram Calculation to Get probability
    probabilities = _histogram(gray_img)

    # Adjust array to contain P(r) values by dividing each element by total_pixels
    for x in range(len(probabilities)):
        probabilities[x] = probabilities[x] / total_pixels

    # Calculate the Entropy
    entropy = _entropy(probabilities)

    return entropy

