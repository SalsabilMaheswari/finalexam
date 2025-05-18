from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,"finalexampredict/home.html")

def about(request):
    return render(request,"finalexampredict/about.html")