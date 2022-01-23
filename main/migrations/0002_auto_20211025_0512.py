# Generated by Django 3.1.3 on 2021-10-25 05:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questions',
            name='downvotes',
            field=models.ManyToManyField(related_name='user_downvote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='questions',
            name='tags',
            field=models.ManyToManyField(to='main.Tags'),
        ),
        migrations.AddField(
            model_name='questions',
            name='upvotes',
            field=models.ManyToManyField(related_name='user_upvote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='answered_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='downvotes',
            field=models.ManyToManyField(related_name='user_a_downvote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question_to_ans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.questions'),
        ),
        migrations.AddField(
            model_name='answer',
            name='upvotes',
            field=models.ManyToManyField(related_name='user_a_upvote', to=settings.AUTH_USER_MODEL),
        ),
    ]
