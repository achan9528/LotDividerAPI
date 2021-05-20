# Generated by Django 2.2.4 on 2021-05-19 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LotDividerAPI', '0008_securityprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='security',
            name='cusip',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='security',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='security',
            name='ticker',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]