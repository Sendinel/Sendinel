from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
    return render_to_response('start.html')
    
def inputText(request):
    return render_to_response('inputText.html')

def chooseCommunication(request):
    return render_to_response('chooseCommunication.html')