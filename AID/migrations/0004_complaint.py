# Generated by Django 5.1.1 on 2024-09-22 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AID', '0003_driver_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.CharField(max_length=90)),
                ('date', models.CharField(max_length=90)),
                ('reply', models.CharField(max_length=90)),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AID.user')),
            ],
        ),
    ]