# Generated by Django 2.2.6 on 2020-02-20 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_proc', '0034_auto_20200220_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=50),
        ),
    ]
