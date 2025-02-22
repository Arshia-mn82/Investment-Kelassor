# Generated by Django 5.1.1 on 2024-09-04 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='FundPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funds.fund')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('start_month', models.CharField(max_length=50)),
                ('end_month', models.CharField(max_length=50)),
                ('final_value', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funds.fund')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
