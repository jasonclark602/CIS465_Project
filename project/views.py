from django.shortcuts import render, get_object_or_404
from .ImageAdjuster import _base, _histogram, EDIT_IMG_PATH
from .forms import *
from PIL import Image as Img


COLORS = ('Red', 'Green', 'Blue', 'RGB')
UPLOADED_IMG = False
IMG_OBJ = None
CONTEXT = {'colors': COLORS, 'form': ImageForm(), 'base': 'RGB'}


# Create your views here.
def index(request, context=None):
    if request.method == 'POST' and not UPLOADED_IMG:
        uploaded_photo(request)

    return render(request, 'index.html', CONTEXT)


def uploaded_photo(request):
    global UPLOADED_IMG, IMG_OBJ
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        UPLOADED_IMG = True
        IMG_OBJ = form.instance

        try:
            image = Img.open('./media/images/project_image.jpg')
            image.save(EDIT_IMG_PATH)
            CONTEXT['url_histogram'] = histogram_url()
        except IOError as e:
            print(e)
            print('Could not duplicate image for edit.')

        CONTEXT['img_url'] = '/media/images/edit.jpg'

    return render(request, 'index.html', CONTEXT)


def histogram_url():
    if UPLOADED_IMG:
        image = Img.open('./media/images/edit.jpg')
        hist = _histogram(image)
        hist.savefig('./media/images/histogram.jpg', format='jpg')
        return '/media/images/histogram.jpg'

    return None


def update_base(request):
    if UPLOADED_IMG:
        base = get_object_or_404(BaseAdjustment, pk=1)
        base.is_gray = not base.is_gray

        if base.is_gray:
            CONTEXT['base'] = 'Gray'
        else:
            CONTEXT['base'] = 'RGB'

        _base(base.is_gray)

    CONTEXT['img_url'] = '/media/images/edit.jpg'
    return render(request, 'index.html', CONTEXT)


def basic(request):
    context = {}

    return render(request, 'index.html', context)


def advanced(request):
    context = {}
