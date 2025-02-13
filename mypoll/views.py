from .models import Choice,Question
from django.shortcuts import render,HttpResponse

def index(request):
    HttpResponse("hello")
    # return render(request,"mypoll/index.html")
    