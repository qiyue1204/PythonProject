from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("欢迎来到韦老师课堂！")
def add(request):
	a=request.GET['a']
	b=request.GET['b']
	c=int(a)+int(b)
	return HttpResponse("结果是:"+str(c))