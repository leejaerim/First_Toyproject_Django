from django.http import JsonResponse
from datetime import datetime
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.views import View
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


@csrf_exempt
def session(request):
    body = json.loads(request.body)
    s = SessionStore()
    if(s.exists(body.get('sid'))):
        s = SessionStore(session_key=body.get('sid'))
        return JsonResponse({
            'id': s.session_key,
            'name': s.get('name')
        })
    else:
        s.create()
        s.set_expiry(0) #expire when browser is closed
        s.setdefault('name', random.choice(nouns))
        s.save()
        return JsonResponse({
            'id': s.session_key,
            'name': s.get('name')
        })
