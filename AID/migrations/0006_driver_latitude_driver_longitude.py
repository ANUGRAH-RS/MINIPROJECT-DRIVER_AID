# Generated by Django 5.1.1 on 2024-09-29 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AID', '0005_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='latitude',
            field=models.CharField(default=1, max_length=90),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='longitude',
            field=models.CharField(default=1, max_length=90),
            preserve_default=False,
        ),
    ]
