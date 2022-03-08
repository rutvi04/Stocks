from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def index(request):
    import requests
    import json

    api_request = requests.get("https://api.polygon.io/v1/open-close/AAPL/2020-10-14?adjusted=true&apiKey=XTRyuTSxOF0KKDoTxdVI5hRSRjGrRB0g")
    try:
        api = json.loads(api_request.content)
    except Exception as e:
        api="Error...."
    #pk_5d448bc5ec78430f9f18a309b283a812
    #XTRyuTSxOF0KKDoTxdVI5hRSRjGrRB0g
    return render(request,'index.html', {'api': api})

def about(request):
    return render(request, 'about.html', {})