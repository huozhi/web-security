from django.shortcuts import render
from precaution import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
# import misaka

DOC_DIR = os.path.join(settings.MEDIA_ROOT, 'doc')

def index(req):
    return render(req, 'index.html', locals())


def xss_script(req, data=''):
    return render(req, 'primary.html', { 'data': data })


def tutorial(req):
    return render(req, 'tutorial.html')
