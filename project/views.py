from PIL import Image as Img
from django.shortcuts import render, get_object_or_404

from .ImageAdjuster import _base, _histogram, entropy, _adjust_brightness, _difference_transformation, _reset
from .constants import *
from .forms import *

SLIDERS = ()
CONTEXT = {}
UPLOADED_IMG = False
STARTUP = True


# Create your views here.
def index(request):
    global STARTUP, SLIDERS, CONTEXT

    if STARTUP:
        val = get_object_or_404(RGBAdjustments, pk=1)
        SLIDERS = (
            Color('Red', val.red_value),
            Color('Green', val.green_value),
            Color('Blue', val.blue_value)
        )

        base = get_object_or_404(BaseAdjustment, pk=1)
        base.is_gray = False
        base.save()

        CONTEXT = {
            'img_obj': EDIT_IMG_PATH,
            'form': ImageForm(),
            'base': 'Gray',
            'sliders_': SLIDERS,
            'diff_txt': 'Difference'
        }
        STARTUP = False

    return render(request, 'index.html', CONTEXT)


def uploaded_photo(request):
    global UPLOADED_IMG, CONTEXT
    if request.method == 'POST' and request.FILES is not None:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            try:
                image = Img.open(PROJ_IMG_PATH)
                image.save(EDIT_IMG_PATH)
            except IOError as e:
                print(e)
                print('Could not duplicate image for edit.')
                raise e

            UPLOADED_IMG = True
            base = get_object_or_404(BaseAdjustment, pk=1)
            base.is_gray = False
            base.save()
            diff = get_object_or_404(Difference, pk=1)
            diff.is_diff = False
            diff.save()

            _histogram()

            CONTEXT.update({
                'url_histogram': str(HIST_IMG_PATH[1:]),
                'img_url': str(EDIT_IMG_PATH[1:]),
                'entropy': entropy(),
            })
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
            CONTEXT['base'] = 'Reset' if base.is_gray else 'Gray'
            CONTEXT['hist_base_txt'] = 'Gray' if base.is_gray else 'RGB'
        elif 'basic' in request.POST:
            rgb = get_object_or_404(RGBAdjustments, pk=1)
            rgb.red_value = int(request.POST['Red_slider'])
            rgb.green_val = int(request.POST['Green_slider'])
            rgb.blue_value = int(request.POST['Blue_slider'])
            rgb.save()

            SLIDERS[0].val = rgb.red_value
            SLIDERS[1].val = rgb.green_val
            SLIDERS[2].val = rgb.blue_value

            _adjust_brightness(rgb.red_value, rgb.green_val, rgb.blue_value)

        elif 'diff_trans' in request.POST:
            diff = get_object_or_404(Difference, pk=1)
            if not diff.is_diff:
                _difference_transformation()
                diff.is_diff = True
                diff.save()
                base.is_gray = True
                base.save()
                CONTEXT['diff_txt'] = 'Reset'
            else:
                _reset()
                diff.is_diff = False
                diff.save()
                base.is_gray = False
                base.save()
                CONTEXT['diff_txt'] = 'Difference'
                CONTEXT['hist_base_txt'] = 'RGB'
        elif 'reset' in request.POST:
            _reset()

        _histogram()
        CONTEXT['entropy'] = entropy()

    return render(request, 'index.html', CONTEXT)
