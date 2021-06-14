from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
import json
import random
nouns = [
    'people',
    'history',
    'way',
    'art',
    'world',
    'information',
    'map',
    'two',
    'family',
    'government',
    'health',
    'system',
    'computer',
    'meat',
    'year',
    'thanks',
    'music',
    'person',
    'reading',
    'method',
    'data',
    'food',
    'understanding',
    'theory',
    'law',
    'bird',
    'literature',
    'problem',
    'software',
    'control',
    'knowledge',
    'power',
    'ability',
    'economics',
    'love',
    'internet',
    'television',
    'science',
    'library',
    'nature',
    'fact',
    'product',
    'idea',
    'temperature',
    'investment',
    'area',
    'society',
    'activity',
    'story',
    'industry',
    'media',
    'thing',
    'oven',
    'community',
    'definition',
    'safety',
    'quality',
    'development',
    'language',
    'management',
    'player',
    'variety',
    'video',
    'week',
    'security',
    'country',
    'exam',
    'movie',
    'organization',
    'equipment',
    'physics',
    'analysis',
    'policy',
    'series',
    'thought',
    'basis',
    'boyfriend',
    'direction',
    'strategy',
    'technology',
    'army',
    'camera',
    'freedom',
    'paper',
    'environment',
    'child',
    'instance',
    'month',
    'truth',
    'marketing',
]

def login(request):
    word = random.choice(nouns)
    res = request.session.session_key 
    if res is not None:
        session_expiry_date = request.session.get_expiry_date().replace(tzinfo=None)
        now = datetime.now()
        seconds_left = (session_expiry_date - now).total_seconds()
        if seconds_left > 0 :
            response =  JsonResponse({'id': res,'nickname':word})
            return response  
        else :
            request.session.create()
            return redirect('http://127.0.0.1:3000/omok/')
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

