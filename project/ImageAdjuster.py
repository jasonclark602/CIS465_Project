# Image and other imports
import numpy as np
import os
from PIL import Image as Img
import math
from .models import Adjustments as Adj, Image


class ImageAdjuster(Image):
    img = Img.open(Image.image)


def _adjust_rgb(Adj, img):
    return 0


def _to_grayscale(img):
    return 0


def _histogram(img):
    histogram = np.zeros(256)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            color = img.getpixel((i, j))
            num = color
            histogram[num] += 1

    return histogram


def _entropy(probabilities):
    num = 0
    for x in probabilities:
        if x == 0:
            continue
        num += x * math.log2(x)

    num *= -1

    return num


def _difference_transormation(img):
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


def calculations(request):
    path = os.path.abspath('.') + '\media\images\project_image.jpg'

    path = path.replace('\\', '/')

    img = Img.open(path)
    entropy = 0
    entropy2 = 0

    gray_img = img.convert("L")
    gray_img.save("./media/images/gray_project_image.jpg")

    total_pixels = gray_img.size[0] * gray_img.size[1]

    # Histogram Calculation to Get probability
    probabilities = _histogram(gray_img)

    # Adjust array to contain P(r) values by dividing each element by total_pixels
    for x in range(len(probabilities)):
        probabilities[x] = probabilities[x] / total_pixels

    # Calculate the Entropy
    entropy = _entropy(probabilities)

    difference_img = _difference_transormation(gray_img)
    difference_img.save("./media/images/difference_image.jpg")

    probabilities2 = _histogram(difference_img)

    # Adjust array to contain P(r) values by dividing each element by total_pixels
    for x in range(len(probabilities2)):
        probabilities2[x] = probabilities2[x] / total_pixels

    # Calculate the Entropy
    entropy2 = _entropy(probabilities2)

    return entropy, entropy2
