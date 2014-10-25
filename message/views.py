from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from message.models import Message

import json

def board(req):
    messages = Message.objects.all()
    return render(req, 'board.html', locals())

@csrf_exempt
def leave_message(req):
    text = None
    if req.is_ajax():
        text = json.loads(req.body)['message']
    try:
        if text is not None:
            message = Message(content=text)
            message.save()
    except Exception, err:
        return HttpResponse(json.dumps('fail'), content_type="application/json")
    return HttpResponse(json.dumps('save'), content_type="application/json")
