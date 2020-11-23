# Image and other imports
import matplotlib
from PIL import Image as Img

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import math

EDIT_IMG_PATH = './media/images/edit.jpg'


def _adjust_rgb():
    return 0


def _base(is_gray):
    if is_gray:
        image = Img.open(EDIT_IMG_PATH).convert('L')
        _histogram(image, is_gray)
        image.save(EDIT_IMG_PATH)
        image.close()
    else:
        image = Img.open('./media/images/project_image.jpg')
        image.save('./media/images/edit.jpg')
        _histogram(image, is_gray)
        image.close()


def _histogram(img, is_gray):
    if not is_gray:
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
        plt.savefig('./media/images/histogram.jpg', format='jpg')
        plt.close()
    else:
        histogram, bin_edges = np.histogram(img, bins=256, range=(0, 256))
        plt.plot(bin_edges[0:-1], histogram, color='k')
        plt.title('Gray Histogram')
        plt.xlabel('Intensity Value')
        plt.ylabel('Pixels')
        plt.savefig('./media/images/histogram.jpg', format='jpg')
        plt.close()


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


def _histogram2(img):
    histogram = np.zeros(256)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color = img.getpixel((i, j))
            num = color
            histogram[num] += 1

    return histogram


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
    probabilities = _histogram2(gray_img)

    # Adjust array to contain P(r) values by dividing each element by total_pixels
    for x in range(len(probabilities)):
        probabilities[x] = probabilities[x] / total_pixels

    # Calculate the Entropy
    entropy = _entropy(probabilities)

    return entropy
