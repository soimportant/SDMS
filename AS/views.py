from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import datetime

# Create your views here.
def current_datetime(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)

'''
def index(request):
'''

def login(request):
	if request.user.is_authenticated:
		message = 'Login successed!'
		return redirect(request, "AS/login.html", locals())
	if request.method == 'POST':
		name = request.POST['username']
		pwd = request.POST['password']
		user = authenticate(username=name, password=pwd)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				return redirect('/AS/index/')
			else:
				message = 'Your account is not active, please login again!'
				return redirect(request, "AS/login.html", locals())
		else:
			message = 'Login failed!'
	return render(request, "AS/login.html", locals())