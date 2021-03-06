# Generated by Django 2.0.5 on 2019-06-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AS', '0002_auto_20190615_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dorminfo',
            name='status',
            field=models.CharField(choices=[('Lived', '有住人'), ('None', '沒有住人'), ('Forbid', '不能住')], default='None', max_length=16),
        ),
        migrations.AlterField(
            model_name='repairment',
            name='category',
            field=models.CharField(choices=[('AC', '冷氣'), ('Furnitures', '家具'), ('Bathroom', '浴室'), ('Internet', '網路'), ('Others', '其他')], max_length=16),
        ),
        migrations.AlterField(
            model_name='repairment',
            name='state',
            field=models.CharField(choices=[('Reported', '已回報'), ('WIP', '修復中'), ('Done', '已完成')], max_length=16),
        ),
        migrations.AlterField(
            model_name='report',
            name='state',
            field=models.CharField(choices=[('Reported', '已回報'), ('WIP', '處理中'), ('Done', '已完成')], max_length=16),
        ),
    ]
