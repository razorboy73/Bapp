from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

# Create your views here.

def index(request):
    context = RequestContext(request)
    context_dict = {"boldmessage": "im bold mofo"}
    return render_to_response('main/index.html', context_dict, context)




