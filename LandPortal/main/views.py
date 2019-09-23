from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
	return render(request=request, template_name="main/index.html")

def about(request):
	return render(request=request, template_name="main/about.html")

def services(request):
	return render(request=request, template_name="main/services.html")

def contact(request):
	return render(request=request, template_name="main/contact.html")

def register(request):
	return render(request=request, template_name="main/register.html")