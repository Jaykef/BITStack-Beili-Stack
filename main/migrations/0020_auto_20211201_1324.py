# Generated by Django 3.1.3 on 2021-12-01 13:24

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20211112_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_image',
            field=models.ImageField(blank=True, null=True, upload_to='posts_pics', validators=[main.models.Posts.validate_file_extension]),
        ),
    ]
