# Generated by Django 2.2.4 on 2021-05-19 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LotDividerAPI', '0007_auto_20210518_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date', models.DateField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('security', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historicalPrices', to='LotDividerAPI.Security')),
            ],
        ),
    ]
