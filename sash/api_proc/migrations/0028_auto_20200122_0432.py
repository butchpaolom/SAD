# Generated by Django 2.2.6 on 2020-01-22 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_proc', '0027_auto_20200122_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='email',
            field=models.EmailField(default='NULL', max_length=254),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='first_name',
            field=models.CharField(default='NULL', max_length=30),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='last_name',
            field=models.CharField(default='NULL', max_length=30),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='middle_initial',
            field=models.CharField(blank=True, default='NULL', max_length=3),
        ),
    ]
