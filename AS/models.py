from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Account(models.Model):

    PERMISSIONS = (
        (0, '系統管理員'),
        (1, '宿舍管理員'),
        (2, '住宿生'),
        (3, '學生')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    permission = models.IntegerField(choices=PERMISSIONS, default=3)
    phone = models.CharField(max_length=10, default='')

    def __str__(self):
        return str(self.user)

class Billboard(models.Model):
    date = models.DateField()
    title = models.CharField(max_length=128)
    publisher = models.ForeignKey('Account', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)


class Repairment(models.Model):
    CATEGORIES = (
        ('AC', '冷氣'),
        ('Furnitures', '家具'),
        ('Bathroom', '浴室'),
        ('Internet','網路'),
        ('Others', '其他')
    )

    STATES = (
        ('Reported', '已回報'),
        ('WIP', '修復中'),
        ('Done', '已完成')
    )

    date = models.DateField()
    publisher = models.ForeignKey('Account', on_delete=models.CASCADE)
    location = models.CharField(max_length=20)
    category = models.CharField(max_length=16, choices=CATEGORIES)
    content = models.CharField(max_length=512)
    state = models.CharField(max_length=16, choices=STATES)


class Report(models.Model):
    CATEGORIES = (
        ('Noise', '噪音'),
        ('Dirty', '髒亂'),
        ('Intrusion', '闖入'),
        ('Others', '其他')
    )

    STATES = (
        ('Reported', '已回報'),
        ('WIP', '處理中'),
        ('Done', '已完成')
    )

    date = models.DateField()
    publisher = models.ForeignKey('Account', on_delete=models.CASCADE)
    accused = models.CharField(max_length=20)
    category = models.CharField(max_length=16, choices=CATEGORIES)
    content = models.CharField(max_length=512)
    state = models.CharField(max_length=16, choices=STATES)


class Conduct(models.Model):
    student = models.ForeignKey('Account', on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    point = models.PositiveSmallIntegerField()
    date = models.DateField()


class StudentInfo(models.Model):
    GENDERS = (
        ('M', '男'),
        ('F', '女')
    )

    GRADES = (
        ('1', '一年級'),
        ('2', '二年級'),
        ('3', '三年級'),
        ('4', '四年級')
    )

    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS)
    department = models.CharField(max_length=16)
    grade = models.CharField(max_length=1, choices=GRADES)
    room = models.CharField(max_length=8, null=True)
    bed = models.IntegerField(null=True)
    conduct = models.PositiveSmallIntegerField(default=0)


class DormRecord(models.Model):
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    Dorms = (
        (0,'綜宿'),
        (1,'OA'),
        (2,'OB'),
        (3,'OE'),
        (4,'OF')
    )
    order1 = models.IntegerField(choices=Dorms)
    order2 = models.IntegerField(choices=Dorms)
    order3 = models.IntegerField(choices=Dorms)

class DormInfo(models.Model):
    STATUS = {
        ('Lived', '有住人'),
        ('None', '沒有住人'),
        ('Forbid', '不能住'),
    }
    GENDERS = (
        ('M', '男'),
        ('F', '女')
    )
    building = models.CharField(max_length=2)
    room = models.CharField(max_length=8)
    bed = models.IntegerField()
    status = models.CharField(max_length=16, choices=STATUS, default='None')
    gender = models.CharField(max_length=1, choices=GENDERS)
    account = models.OneToOneField(
        'Account', on_delete=models.SET_NULL, null=True)


class BillInfo(models.Model):
    STATES = (
        ('Unpaid', '未繳費'),
        ('Paid', '已繳費'),
        ('Expired', '過期')
    )

    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    year = models.CharField(max_length=4)
    content = models.CharField(max_length=512)
    state = models.CharField(max_length=10, choices=STATES)



class Equipment(models.Model):
    STATES = (
        ('Free', '可借用'),
        ('InUse', '出借中'),
        ('NotAvailable', '不可使用')
    )


    tag = models.CharField(max_length = 16, primary_key = True)
    name = models.CharField(max_length = 20)
    current_state = models.CharField(max_length = 16, choices = STATES)


class BorrowRecord(models.Model):

    STATES = (
        (0, '等待核可中'),
        (1, '核可完成'),
        (2, '退件')
    )

    tag = models.ForeignKey('Equipment', on_delete = models.CASCADE)
    account = models.ForeignKey('Account', on_delete = models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    memo = models.CharField(max_length = 512)
    confirm = models.IntegerField(choices = STATES)


class Package(models.Model):
    CATEGORIES = (
        ('Mail', '信件'),
        ('Package', '包裹'),
        ('Prompt', '限時')
    )

    date = models.DateField(auto_now=True)
    category = models.CharField(max_length = 10, choices = CATEGORIES)
    receiver = models.ForeignKey('Account', on_delete = models.CASCADE)
    sender = models.CharField(max_length = 32)
    verify = models.BooleanField(default = False)
class System(models.Model):
    StartTime = models.DateField()
    EndTime = models.DateField()

