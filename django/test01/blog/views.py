from django.shortcuts import render

# Create your views here.
from django.http  import HttpResponse
#req: request info
def index(req):
    return HttpResponse('<h1>hello</h1>')

