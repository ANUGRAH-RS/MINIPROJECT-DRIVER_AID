# Generated by Django 5.1.1 on 2024-10-27 13:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AID', '0011_complaint_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='DRIVER',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='AID.driver'),
            preserve_default=False,
        ),
    ]
