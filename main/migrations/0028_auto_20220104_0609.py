# Generated by Django 3.1.3 on 2022-01-04 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20220103_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='upvote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='upvote',
            name='user',
        ),
        migrations.DeleteModel(
            name='DownVote',
        ),
        migrations.DeleteModel(
            name='UpVote',
        ),
    ]
