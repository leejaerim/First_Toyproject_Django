from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
import json


def login(request):
    res = request.session.session_key 
    if res is not None:
        session_expiry_date = request.session.get_expiry_date().replace(tzinfo=None)
        now = datetime.now()
        seconds_left = (session_expiry_date - now).total_seconds()
        if seconds_left > 0 :
            response =  JsonResponse({'id': res})
            return response  
        else :
            return HttpResponse("Session was expired.")
    else:
        request.session.create()
        return redirect('http://127.0.0.1:3000/omok/')

    # res = request.session.session_key
    # return HttpResponse(json.dumps(res), 'application/json')

    # JsonResponse({'session_expired': True, 'seconds_left': seconds_left })
    # if request.session.has_key:
    #     session_key = request.session.session_key
    #     session = Session.objects.get(session_key = session_key)
    #     print()
    #     # uid = session.get_decoded().get('user')
    # else
    #     # request.session.crete()
    # session = Session.objects.get(session_key = session_key)
    #     data = session.get_decoded()

