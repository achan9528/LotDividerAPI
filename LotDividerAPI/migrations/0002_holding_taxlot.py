# Generated by Django 2.2.4 on 2021-05-07 20:30

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LotDividerAPI', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=uuid.uuid4, max_length=50)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='LotDividerAPI.Account')),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatedHoldings', to='LotDividerAPI.Security')),
            ],
        ),
        migrations.CreateModel(
            name='TaxLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=uuid.uuid4, max_length=50)),
                ('units', models.DecimalField(decimal_places=4, max_digits=20)),
                ('totalFederalCost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('totalStateCost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('acquisitionDate', models.DateTimeField(auto_now_add=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('holding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taxLots', to='LotDividerAPI.Holding')),
            ],
        ),
    ]
