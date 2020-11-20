from django.shortcuts import render, redirect

from .forms import *

COLORS = ('red', 'green', 'blue', 'rgb')


# Create your views here.
def index(request):
    if request.method == 'POST':
        if request.FILES:
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                image_field = form.cleaned_data
                form.save()
        else:
            for c in COLORS:
                print(request.POST[c + '_slider'])

        return redirect('project/index.html')

    else:
        form = ImageForm()

    context = {
        'form': form,
        'image_name': 'project_image.jpg',
        'colors': COLORS
    }

    return render(request, 'project/index.html', context)

