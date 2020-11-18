from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .forms import *


# Create your views here. 
def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

    else:
        form = ImageForm()

    template = loader.get_template('../templates/index.html')
    context = {'form': form}
    return render(request, 'index.html', context)


def image_view(request):
    return HttpResponse('img')
