from django.http import HttpResponse

from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import *
  
# Create your views here. 
def image_view(request): 
  
    if request.method == 'POST': 
        form = ImageForm(request.POST, request.FILES) 
  
        if form.is_valid(): 
            form.save() 
            return redirect('calculations') 
    else: 
        form = ImageForm() 
    return render(request, 'home.html', {'form' : form}) 
  
  
def calculations(request): 
    return render(request, 'calculations.html')
