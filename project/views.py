from django.shortcuts import render, redirect

from .forms import *

COLORS = ('red', 'green', 'blue', 'rgb')


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        context = {
            'form': form,
            'colors': COLORS
        }
        if form.is_valid():
            form.save()
            img_obj = form.instance
            context['img_obj'] = img_obj

        else:
            for c in COLORS:
                print(request.POST[c + '_slider'])

        return render(request, 'project/index.html', context)

    else:
        form = ImageForm()

    context = {
        'form': form,
        'colors': COLORS
    }

    return render(request, 'project/index.html', context)

