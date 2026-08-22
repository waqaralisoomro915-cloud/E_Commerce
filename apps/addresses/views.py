from django.shortcuts import render
from django.http import HttpResponse
def addresses(request):
    return HttpResponse("Hello, world. You're at the address book.")

