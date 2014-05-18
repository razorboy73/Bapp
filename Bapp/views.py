from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)