# Generated by Django 2.0.5 on 2019-05-31 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AS', '0003_auto_20190529_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='DormInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=2)),
                ('room', models.CharField(max_length=8)),
                ('bed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DormRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order1', models.IntegerField(choices=[(0, '綜合'), (1, '學一'), (2, '學二')])),
                ('order2', models.IntegerField(choices=[(0, '綜合'), (1, '學一'), (2, '學二')])),
                ('order3', models.IntegerField(choices=[(0, '綜合'), (1, '學一'), (2, '學二')])),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='id',
        ),
        migrations.RemoveField(
            model_name='studentinfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='studentinfo',
            name='studentID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='AS.Account'),
        ),
        migrations.AddField(
            model_name='dormrecord',
            name='studentID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AS.StudentInfo'),
        ),
        migrations.AddField(
            model_name='dorminfo',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='AS.StudentInfo'),
        ),
    ]
