# Generated by Django 3.1.3 on 2022-01-13 07:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0036_auto_20220113_0733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='favourites',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='questions',
            name='likes',
        ),
        migrations.AddField(
            model_name='posts',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='posts',
            name='like_count',
            field=models.BigIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.ManyToManyField(blank=True, default=None, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]
