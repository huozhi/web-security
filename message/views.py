from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse('hello')

def home(request):
    return render(request, 'board.html')
