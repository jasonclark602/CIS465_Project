# models.py 
from django.db import models
import hashlib
import datetime
import os
from functools import partial

def _update_filename(instance, filename, path):
    path = path

    filename = "project_image.jpg"

    return os.path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)

class Image(models.Model): 
    name = models.CharField(max_length=50) 
    image = models.ImageField(upload_to=upload_to('images/'))