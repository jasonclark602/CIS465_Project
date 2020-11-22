from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .ImageAdjuster import _base, _histogram
from .forms import *
from PIL import Image as Img
from .models import Image

COLORS = ('Red', 'Green', 'Blue', 'RGB')
UPLOADED_IMG = False
M_ROOT = settings.MEDIA_ROOT
IMG_ROOT = M_ROOT + 'images/'
IMG_OBJ = None


def uploaded_photo(request):
    global UPLOADED_IMG, IMG_OBJ
    form = ImageForm(request.POST, request.FILES)
    context = {'colors': COLORS, 'form': form}
    if form.is_valid():
        form.save()
        UPLOADED_IMG = True
        IMG_OBJ = form.instance

        try:
            image = Img.open('./media/images/project_image.jpg')
            image.save('./media/images/edit.jpg')
            context['url_histogram'] = histogram_url()
        except IOError as e:
            print(e)
            print('Could not duplicate image for edit.')

        context['img_obj'] = IMG_OBJ

    return index(request, context)


def histogram_url():
    if UPLOADED_IMG:
        path = './media/images/project_image.jpg'
        image = Img.open(path)
        hist = _histogram(image)
        hist.savefig('./media/images/histogram.jpg', format='jpg')
        return '/media/images/histogram.jpg'

    return ''


# Create your views here.
def index(request, context=None):
    if context is None:
        context = {}

    if request.method == 'POST' and not UPLOADED_IMG:
        uploaded_photo(request)

    context['form'] = ImageForm()

    return render(request, 'index.html', context)


def update_base(request):
    if UPLOADED_IMG:
        basic_obj = get_object_or_404(BasicForm, pk=1)
        basic_obj.base.is_gray = not basic_obj.base.is_gray
        isGray = basic_obj.base.is_gray
        _base(isGray)

    return index(request)


def basic(request):
    context = {}

    return render(request, 'index.html', context)


def advanced(request):
    context = {}
