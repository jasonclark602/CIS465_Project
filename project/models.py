# models.py 
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import hashlib
import datetime
import os
from functools import partial


def _update_filename(instance, filename, path):
    path = path

    filename = 'project_image.jpg'

    return os.path.join(path, filename)


def upload_to(path):
    return partial(_update_filename, path=path)


class OverwriteStorage(FileSystemStorage):
    '''
    Overwrites the file name project_image if it already exits
    '''

    def get_available_name(self, name, max_length=500):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class Image(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_to('images/'), storage=OverwriteStorage())
    # Duplicate image for editing

