from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
import os
from functools import partial


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


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


class Adjustments(models.Model):
    gray = models.BooleanField(default=False)
    adjustment = models.CharField(max_length=12)
    red_value = models.IntegerField(default=200)
    green_value = models.IntegerField(default=200)
    blue_value = models.IntegerField(default=200)
    gamma = models.IntegerField(default=0.5)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


