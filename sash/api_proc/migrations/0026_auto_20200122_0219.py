# Generated by Django 2.2.6 on 2020-01-22 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_proc', '0025_auto_20200122_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='finalorder',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'COD'), (2, 'PayPal')], null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Packaging'), (2, 'In Transit'), (3, 'Out for Delivery')], null=True),
        ),
    ]