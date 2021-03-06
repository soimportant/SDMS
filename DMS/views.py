from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from AS.models import Account, StudentInfo, DormRecord, DormInfo, BillInfo, System
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import *
import datetime
import random


@login_required(login_url='/AS/login/')
def DormSetting(request):
    ac = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=ac)
        lived = True
    except:
        lived = False

    if ac.permission != 0:
        error = "權限不符"
        return redirect('/DMS/main/')
    time = System.objects.get(pk=1)
    if request.method == 'POST':
        try:
            start = request.POST['StartTime']
            end = request.POST['EndTime']
            time.StartTime = start
            time.EndTime = end
            time.save()
            message = "修改成功"
        except:
            error = "格式不符"
    time = System.objects.get(pk=1)
    return render(request, 'DMS/DormSetting.html', locals())


def Delete(request):
    # DormRecord.objects.all().delete()
    return redirect('/DMS/main/')


@login_required(login_url='/AS/login/')
def main(request,message='',error=''):
    name = request.user.username
    ac = Account.objects.get(user=request.user)
    if ac.permission <= 1:  # 管理員
        Permission = True
    else:
        Permission = False

    dorm = {
        'status': '無住宿',
        'bed': '無',
        'building': '無',
        'room': '無'
    }
    try:
        dorminfo = DormInfo.objects.get(account=ac)
        dorm['status'] = '入住中'
        dorm['building'] = dorminfo.building
        dorm['room'] = dorminfo.room
        dorm['bed'] = dorminfo.bed
        lived = True
    except:
        dorm['status'] = '無住宿'
        lived = False
    return render(request, "DMS/main.html", locals())


@login_required(login_url='/AS/login/')
def DormRetreatApply(request):
    account = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=account)
        lived = True
    except:
        lived = False
    return render(request, 'DMS/DormRetreatApply.html', locals())


@login_required(login_url='/AS/login/')
def DormitoryApply(request):
    # 判斷是否為管理員
    name = request.user.username
    ac = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=ac)
        lived = True
    except:
        lived = False

    try:
        gender = StudentInfo.objects.get(account=ac).gender
        if gender == 'M':
            gd = True
    except:
        gd = True
    TIME = System.objects.get(pk=1)
    start = TIME.StartTime
    end = TIME.EndTime
    now = datetime.date.today()
    if now > start and now < end:  # 開放
        # 誰申請 哪個系 年級 學號 姓名 哪一棟宿舍 申請時間 審核狀態
        # 宿舍房間狀況 eg. OF 5層樓 20個房間 4個人
        return render(request, "DMS/DormitoryApply.html", locals())
    else:  # 不開放
        message = "目前並未開放申請宿舍。"
        return redirect('/DMS/main/')


@login_required(login_url='/AS/login/')
def DormCheck(request):
    name = request.user.username
    account = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=account)
        lived = True
    except:
        lived = False

    try:
        gender = StudentInfo.objects.get(account=account).gender
        if gender == 'M':
            gd = True
    except:
        gd = True
    if account.permission == 0:  # 管理員
        DormRecords = DormRecord.objects.all()
        dorms = []
        for dormRecord in DormRecords:
            try:
                dorm = DormInfo.objects.get(account=dormRecord.account)
                result = dorm.building+dorm.room+"-"+str(dorm.bed)
            except:
                TIME = System.objects.get(pk=1)
                now = datetime.date.today()
                end = TIME.EndTime
                if now > end:
                    result = "未抽中床位"
                else:
                    result = "尚未開始分發"
            dm = {
                'D1': DormRecord.Dorms[dormRecord.order1][1],
                'D2': DormRecord.Dorms[dormRecord.order2][1],
                'result': result
            }
            try:
                dm.setdefault('D3', DormRecord.Dorms[dormRecord.order3][1])
            except:
                dm.setdefault('D3', '')
            dorms.append(dm)
        paginator = Paginator(dorms, 100)
        page = request.GET.get('page')
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        return render(request, "DMS/DormCheck.html", locals())
    elif request.method == 'POST':  # 學生
        TIME = System.objects.get(pk=1)
        start = TIME.StartTime
        end = TIME.EndTime
        now = datetime.date.today()
        name = request.user.username
        D1 = request.POST['Dorm1']
        D2 = request.POST['Dorm2']
        try:
            D3 = request.POST['Dorm3']
        except:
            D3 = 9
        if D1 == D2 or D2 == D3 or D1 == D3:
            error = "志願序不可重複。"
            return render(request, "DMS/DormitoryApply.html", locals())
        else:
            try:
                student = StudentInfo.objects.get(account=account)
            except:
                error = "此用戶並非學生。"
                return render(request, "DMS/DormitoryApply.html", locals())
            if DormRecord.objects.filter(account=account):
                error = "不可重複申請。"
                return render(request, "DMS/DormitoryApply.html", locals())
            with transaction.atomic():
                DormRecord.objects.create(
                    account=account, order1=D1, order2=D2, order3=D3)
                message = "申請成功。"
                return redirect('/DMS/main/')
    else:
        ac = Account.objects.get(user=request.user)
        try:
            dorm = DormRecord.objects.get(account=ac)
        except:
            error = "查無此資料。"
            return redirect('/DMS/main/')
        D1 = DormRecord.Dorms[dorm.order1][1]
        D2 = DormRecord.Dorms[dorm.order2][1]
        try:
            D3 = DormRecord.Dorms[dorm.order3][1]
        except:
            D3 = ''
        try:
            dorminfo = DormInfo.objects.get(account=ac)
            result = dorminfo.building + \
                dorminfo.room + "-" + str(dorminfo.bed)

        except:
            TIME = System.objects.get(pk=1)
            end = TIME.EndTime
            now = datetime.date.today()
            if now < end:
                result = "尚未分發"
            else:
                result = "未抽中床位"
        try:
            student = StudentInfo.objects.get(account=ac)
        except:
            error = "此用戶並非學生。"
            return redirect('/DMS/main/')
        dorms = []
        dm = {
            'D1': D1,
            'D2': D2,
            'D3': D3,
            'result': result
        }
        dorms.append(dm)
        paginator = Paginator(dorms, 100)
        page = request.GET.get('page')
        now = datetime.date.today()
        TIME = System.objects.get(pk=1)
        start = TIME.StartTime
        end = TIME.EndTime
        if now > start and now < end:  # 宿舍申請期間
            checked = 0
        elif now < end+datetime.timedelta(days=7):  # 截止7天之內
            if result != "未抽中床位":
                checked = 1
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)
        return render(request, "DMS/DormCheck.html", locals())


@login_required(login_url='/AS/login/')
def DormRetreat(request, username=''):
    ac = Account.objects.get(user=request.user)
    account = ac
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=ac)
        lived = True
    except:
        lived = False
    if ac.permission == 0:  # 管理員
        Permission = True
    else:
        error = "權限不符。"
        return redirect('/DMS/main/', error=error)
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
        except:
            message = "查無該學號。"
            return render(request, 'DMS/Retreat.html', locals())
        student = {}
        student['name'] = user.username
        ac = Account.objects.get(user=user)
        try:
            dorm = DormInfo.objects.get(account=ac)
        except:
            message = "該學生並非住宿生。"
            return render(request, 'DMS/Retreat.html', locals())
        student['building'] = dorm.building
        student['bed'] = dorm.bed
        student['room'] = dorm.room
        Check = True
        return render(request, 'DMS/Retreat.html', locals())
    if username == '':  # 導向住宿學生名單
        return render(request, "DMS/Retreat.html", locals())
    user = User.objects.get(username=username)
    ac = Account.objects.get(user=user)
    try:
        ac.permission = 3
        ac.save()
        Dorm = DormInfo.objects.get(account=ac)
        Dorm.account = None
        Dorm.status = 'None'
        Dorm.save()
        # Dorm.delete()
        message = "退宿成功。"
        return render(request, 'DMS/Retreat.html', locals())
    except:
        message = "查無該學生宿舍資料。"
        return redirect('/DMS/main/', message=message)


@login_required(login_url='/AS/login/')
def DormDelete(request):
    ac = Account.objects.get(user=request.user)
    try:
        dm = DormRecord.objects.get(account=ac)
        dm.delete()
        message = "刪除成功。"
        return redirect('/DMS/main/')
    except:
        error = "查無此資料。"
        return redirect('/DMS/main/')


@login_required(login_url='/AS/login')
def Retreat(request):
    ac = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=ac)
        lived = True
    except:
        lived = False

    ac.permission = 3
    ac.save()
    dorm = DormInfo.objects.get(account=ac)
    dorm.account = None
    dorm.status = 'None'
    dorm.save()
    message = "退宿成功。"
    return render(request, 'DMS/DormCheck.html', locals())


""""
def StudentPermission(request):
    dorms = DormInfo.objects.all()
    count = 0
    for dorm in dorms:
        ac = dorm.account
        ac.permission = 2
        ac.save()
        count+=1
        print(count)
    return redirect('/DMS/main/')
"""
@login_required(login_url='/AS/login/')
def DormDistribution(request):
    account = Account.objects.get(user=request.user)
    lived = False
    try:
        dorminfo = DormInfo.objects.get(account=account)
        lived = True
    except:
        lived = False

    if account.permission != 0:
        error = "你沒有使用本頁面的權限。"
        return redirect('/DMS/main/')
    if request.method != "POST":
        TIME = System.objects.get(pk=1)
        start = TIME.StartTime
        end = TIME.EndTime
        return render(request, 'DMS/DormDistribution.html', locals())
    DormRecords = DormRecord.objects.all().order_by('?')
    # 先分發志願序一
    count = 0
    for Record in DormRecords:
        Student = StudentInfo.objects.get(account=Record.account)
        try:
            if DormInfo.objects.get(account=Record.account) != None:
                continue
        except:
            try:
                D1 = DormInfo.objects.filter(
                    account__isnull=True, building=Record.Dorms[Record.order1][1], gender=Student.gender)[0]
                D1.account = Student.account
                D1.status = 'Lived'
                D1.save()
            except:
                try:
                    D2 = DormInfo.objects.filter(account__isnull=True, building=Record.Dorms[Record.order2][1],
                                                 gender=Student.gender)[0]
                    D2.account = Student.account
                    D2.status = 'Lived'
                    D2.save()
                except:
                    try:
                        D3 = DormInfo.objects.filter(account__isnull=True, building=Record.Dorms[Record.order3][1],
                                                     gender=Student.gender)[0]
                        D3.account = Student.account
                        D3.status = 'Lived'
                        D3.save()
                    except:
                        print("QQ")
            print(count)
            count += 1
    return redirect('/DMS/main/')


"""
@login_required(login_url='/AS/login/')
def BillCreate(request):
    account = Account.objects.get(user=request.user)
    if account.permission != 0:
        error = "權限不符"
        return render(request, 'AS/main.html', locals())
    Students = DormInfo.objects.all()
    year = datetime.datetime.now().year
    for Student in Students:
        content = Student.building
        BillInfo.objects.create(account=Student.account,year=year,content=content,state='Unpaid')
    return render(request,'DMS/main.html',locals())
"""
"""
def DormInfoCreate(request):
    # OE 280 男 1~5  14rooms/floor
    # OA1 240 男 1~4 15rooms/floor
    # 綜宿 320 男  3~4 40rooms/floor
    # OF 280 女 1~5 14rooms/floor
    # OA2 128 女 5~6 16rooms/floor
    # OB 360 女 1~6 15rooms/floor
    for i in range(1,7):
        for j in range(1,16):
            for k in range(1,5):
                DormInfo.objects.create(building="OB",room=str(i)+str(j).zfill(2),bed=k,status='None',gender='F')
                print(i,j,k)

    return render(request,"DMS/DMS.html",locals())
"""
"""
def DormRecordCreate(request):
    Students = StudentInfo.objects.all()
    i = 0
    for Student in Students:
        ac = Student.account
        try:
            DormRecord.objects.get(account=ac)  ##該學生已經申請過了
        except:
            if Student.gender=='M':
                seq = [0,1,3]
                order = random.sample(seq,k=3)
                DormRecord.objects.create(account=ac,order1=order[0],order2=order[1],order3=order[2])
            else:
                seq = [1,2,4]
                order = random.sample(seq,k=3)
                DormRecord.objects.create(account=ac,order1=order[0],order2=order[1],order3=order[2])
        print(i)
        i+=1

    return redirect('/DMS/main/')
"""
