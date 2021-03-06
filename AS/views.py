from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime
from .models import *

# Create your views here.
def index(request):
	billboard = Billboard.objects.all().order_by("-date")[:5]
	try:
		account = Account.objects.get(user=request.user)
	except:
		return render(request, 'AS/index.html', locals())

	lived = False
	try:
		dorminfo = DormInfo.objects.get(account=account)
		lived = True
	except:
		lived = False
		return render(request, 'AS/index.html', locals())

	pk_num = len(Package.objects.filter(receiver=Account.objects.get(user=auth.get_user(request))))
	now_conduct = StudentInfo.objects.get(account=account).conduct

	return render(request, 'AS/index.html', locals())


def current_datetime(request):
	now = datetime.datetime.now()
	html = '<html><body>It is now %s.</body></html>' % now
	return HttpResponse(html)

def convert_permission(perID):
	'''
	PERMISSIONS = (
        (0, '系統管理員'),
        (1, '宿舍管理員'),
        (2, '住宿生'),
        (3, '學生')
    )
	'''
	convert_table = ['系統管理員', '宿舍管理員', '住宿生', '學生']
	return convert_table[perID]

@login_required(login_url='/AS/login/')
def main(request):
	user = request.user
	stu_id = user.username
	name = user.last_name+user.first_name
	account = Account.objects.get(user=user)
	permission = convert_permission(account.permission)
	phone = account.phone
	mail = user.email
	message='登入成功。'
	return render(request, 'AS/main.html', locals())

def login(request):
	message = ''
	if request.user.is_authenticated:
		return redirect('/AS/main/')
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=name, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				return redirect('/AS/main/')		
			else:
				message = '此帳戶目前不可用。如有任何問題，請聯絡管理員。'
				return render(request, 'AS/login.html', locals())
		else:
			message = '登入失敗。請檢查你的帳號或密碼是否有誤。'
	return render(request, 'AS/login.html', locals())

@login_required(login_url='/AS/login/')
def logout(request):
	auth.logout(request)
	return redirect('/AS/login/')
	message = '登出成功。'

@login_required(login_url='/AS/login/')
def modify(request):
	user = request.user
	account = Account.objects.get(user=user)
	stu_id = user.username
	fname = user.first_name
	lname = user.last_name
	phone = account.phone
	mail = user.email
	if request.method == 'POST':
		new_fname = request.POST['firstname']
		new_lname = request.POST['lastname']
		new_phone = request.POST['phone']
		new_mail = request.POST['email']
		if fname != new_fname and new_fname != '':
			user.first_name = fname
			user.save()
		if lname != new_lname and new_lname != '':
			user.last_name = lname
			user.save()
		if phone != new_phone and new_phone != '':		
			account.phone = new_phone
			account.save()
		if mail != new_mail and new_mail != '':
			user.email = new_mail
			user.save()
		return redirect("/AS/main/")
	else:		
		return render(request,"AS/modify.html",locals())

@login_required(login_url='/AS/login/')
def modify_password(request):
	user = request.user
	username = user.username
	account = Account.objects.get(user=user)
	message = ''
	if request.method == 'POST':
		curpass = request.POST['current_pass']
		npass = request.POST['new_pass']	
		chpass = request.POST['check_pass']
		
		if not user.check_password(curpass):				
			message = "目前密碼錯誤。"
			return render(request,"AS/modify_password.html",locals())

		if npass != chpass:
			message = "新密碼確認失敗。請檢查兩次輸入是否有誤。"
			return render(request,"AS/modify_password.html",locals())
		else:
			message = "密碼修改成功。"
			return render(request,"AS/modify_password.html",locals())
		user.set_password(npass)
		user.save()
		User = authenticate(username=username, password=npass)
		auth.login(request,User)
		return redirect("/AS/main/")
	else :
		return render(request,"AS/modify_password.html",locals())