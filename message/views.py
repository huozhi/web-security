from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from message.models import Message

def board(req):
    messages = Message.objects.all()
    return render(req, 'board.html', locals())
