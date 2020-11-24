import os
from functools import partial

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


# Create your models here
def _update_filename(instance, filename, path):
    path = path

    filename = "project_image.jpg"

    return os.path.join(path, filename)


def upload_to(path):
    return partial(_update_filename, path=path)


class OverwriteStorage(FileSystemStorage):
    """
    Overwrites the file name project_image if it already exits
    """

    def get_available_name(self, name, max_length=500):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to('images/'), storage=OverwriteStorage())


class BaseAdjustment(models.Model):
    is_gray = models.BooleanField(default=False)


class RGBAdjustments(models.Model):
    red_value = models.IntegerField(default=100)
    green_value = models.IntegerField(default=100)
    blue_value = models.IntegerField(default=100)


class Difference(models.Model):
    is_diff = models.BooleanField(default=False)


class Color:
    def __init__(self, name, val):
        self.name = name
        self.val = val
