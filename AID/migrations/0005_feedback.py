# Generated by Django 5.1.1 on 2024-09-22 13:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AID', '0004_complaint'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=90)),
                ('date', models.CharField(max_length=90)),
                ('rating', models.CharField(max_length=90)),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AID.user')),
            ],
        ),
    ]
