# Generated by Django 2.2.6 on 2019-10-10 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_proc', '0015_auto_20191010_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image1',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]