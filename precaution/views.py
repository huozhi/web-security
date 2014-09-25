from django.shortcuts import render

def index(req):
    return render(req, 'index.html', locals())


def primary_xss(req, data='SCRIPT'):
    return render(req, 'primary.html', { 'data': data })