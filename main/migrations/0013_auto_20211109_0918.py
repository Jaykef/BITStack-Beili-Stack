# Generated by Django 3.1.3 on 2021-11-09 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20211109_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comments',
        ),
        migrations.AddField(
            model_name='posts',
            name='comments',
            field=models.ManyToManyField(related_name='comments', to='main.Comment'),
        ),
    ]
