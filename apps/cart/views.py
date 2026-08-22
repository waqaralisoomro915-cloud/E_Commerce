from django.shortcuts import render
from django.http import HttpResponse

def cart(request):
    return HttpResponse("this is cart view")