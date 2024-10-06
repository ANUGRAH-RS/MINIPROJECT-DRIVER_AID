# Generated by Django 5.1.1 on 2024-10-06 08:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AID', '0007_driver_availability'),
    ]

    operations = [
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.CharField(max_length=90)),
                ('date', models.DateField()),
                ('fromid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kk', to='AID.login_table')),
                ('toid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ll', to='AID.login_table')),
            ],
        ),
    ]