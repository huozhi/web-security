from django.shortcuts import render

def index(req):
    return render(req, 'index.html', locals())


def xss_script(req, data='INJECTION'):
    return render(req, 'primary.html', { 'data': data })
