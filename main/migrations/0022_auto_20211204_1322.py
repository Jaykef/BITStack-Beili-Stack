# Generated by Django 3.1.3 on 2021-12-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20211204_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='posted_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
