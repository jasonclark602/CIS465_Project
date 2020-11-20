from django.shortcuts import render, redirect

from .forms import *
import numpy as np
import os
from PIL import Image as Img
import math
from .models import Adjustments as Adj, Image


COLORS = ('red', 'green', 'blue', 'rgb')
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


def calculations():
    path = os.path.abspath('.') + '\media\images\project_image.jpg'

    path = path.replace('\\', '/')

    img = Img.open(path)
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

# Create your views here.
def index(request):
    entropy = calculations()
    if request.method == 'POST':
        if request.FILES:
            form = ImageForm(request.POST, request.FILES)
            
            context = {
            'form': form,
            'colors': COLORS,
            'entropy':entropy,
            }

            if form.is_valid():
                form.save()
                img_obj = form.instance
                context['img_obj'] = img_obj
                

                
        else:
            for c in COLORS:
                print(request.POST[c + '_slider'])

        return render(request, 'index.html', context)

    else:
        form = ImageForm()

    
    context = {
        'form': form,
        'image_name': 'project_image.jpg',
        'colors': COLORS,
        'entropy': entropy,
     
        
    }
    
    return render(request, 'index.html', context)

