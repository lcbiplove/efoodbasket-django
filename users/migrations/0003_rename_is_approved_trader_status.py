# Generated by Django 3.2.6 on 2021-08-29 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210828_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trader',
            old_name='is_approved',
            new_name='status',
        ),
    ]
