# Generated by Django 3.1.3 on 2021-11-09 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20211109_0932'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post_to_comment',
        ),
    ]
