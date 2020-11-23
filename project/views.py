from django.shortcuts import render, get_object_or_404
from .ImageAdjuster import _base, _histogram, entropy, _adjust_brightness, _difference_transformation
from .forms import *
from PIL import Image as Img
from .constants import *

COLORS = ()
CONTEXT = {}
UPLOADED_IMG = False
STARTUP = True


# Create your views here.
def index(request):
    global STARTUP, COLORS, CONTEXT

    if STARTUP:
        rgb = get_object_or_404(RGBAdjustments, pk=1)
        COLORS = (
            Color('Red', rgb.red_value),
            Color('Green', rgb.green_value),
            Color('Blue', rgb.blue_value)
        )

        base = get_object_or_404(BaseAdjustment, pk=1)
        base_str = 'Gray' if base.is_gray else 'RGB'

        CONTEXT = {
            'colors': COLORS,
            'img_obj':  EDIT_IMG_PATH,
            'form': ImageForm(),
            'base': base_str
        }
        STARTUP = False

    return render(request, 'index.html', CONTEXT)


def uploaded_photo(request):
    if request.method == 'POST' and request.FILES is not None:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            try:
                image = Img.open(PROJ_IMG_PATH)
                image.save(EDIT_IMG_PATH)
                global UPLOADED_IMG
                UPLOADED_IMG = True
                base = get_object_or_404(BaseAdjustment, pk=1)
                base.is_gray = False
                base.save()
                diff = get_object_or_404(Difference, pk=1)
                diff.is_diff = False
                diff.save()
            except IOError as e:
                print(e)
                print('Could not duplicate image for edit.')
                raise e

            _histogram(False)
            CONTEXT['url_histogram'] = str(HIST_IMG_PATH[1:])
            CONTEXT['img_url'] = str(EDIT_IMG_PATH[1:])
            CONTEXT['entropy'] = entropy()
    else:
        index(request)

    return render(request, 'index.html', CONTEXT)


def update(request):
    if UPLOADED_IMG:
        base = get_object_or_404(BaseAdjustment, pk=1)
        if 'base' in request.POST:
            base.is_gray = not base.is_gray
            base.save()
            _base(base.is_gray)
            CONTEXT['base'] = 'Gray' if base.is_gray else 'RGB'

        elif 'basic' in request.POST:
            rgb = get_object_or_404(RGBAdjustments, pk=1)
            rgb.red_value = int(request.POST['Red_slider'])
            rgb.green_val = int(request.POST['Green_slider'])
            rgb.blue_value = int(request.POST['Blue_slider'])
            rgb.save()

            _adjust_brightness(rgb.red_value, rgb.green_val, rgb.blue_value)

        elif 'diff_trans' in request.POST:
            diff = get_object_or_404(Difference, pk=1)
            if not diff.is_diff:
                _difference_transformation()
                diff.is_diff = True
                diff.save()
                base.is_gray = True
                base.save()

        _histogram(base.is_gray)
        CONTEXT['entropy'] = entropy()

    return render(request, 'index.html', CONTEXT)
