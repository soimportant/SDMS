# Generated by Django 2.0.5 on 2019-06-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AS', '0004_dorminfo_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipment',
            name='category',
        ),
        migrations.AddField(
            model_name='equipment',
            name='name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]