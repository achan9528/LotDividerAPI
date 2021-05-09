# Generated by Django 2.2.4 on 2021-05-08 16:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LotDividerAPI', '0005_draftholding'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftTaxLot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=uuid.uuid4, max_length=50)),
                ('units', models.DecimalField(decimal_places=4, max_digits=20)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('draftHolding', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draftTaxLots', to='LotDividerAPI.DraftHolding')),
                ('referencedLot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='draftTaxLotsRelated', to='LotDividerAPI.TaxLot')),
            ],
        ),
    ]