# Generated by Django 4.2.1 on 2023-05-10 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_alter_friendrequest_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='status',
        ),
    ]
