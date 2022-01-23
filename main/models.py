from django.db import models
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
# from userauth.models import User
medium_len = 100
long_len = 255


class Tags(models.Model):
    tag_word = models.CharField(max_length=medium_len, unique = True,  default='BITStack')  

class Questions(models.Model):
    title = models.CharField(max_length=long_len)
    ques_content = models.TextField()
    tags = models.ManyToManyField(Tags)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_upvote')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_downvote')
    answers = models.ManyToManyField('main.Answer', related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    views = models.IntegerField(default=0)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)
    has_accepted_answer = models.BooleanField(default=False)

    thumbsup = models.IntegerField(default='0')
    thumbsdown = models.IntegerField(default='0')
    thumbs = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thumbs', default=None, blank=True)


    def get_date(self):
        time = datetime.now()
        if self.created_at.minute == time.minute:
            return str(time.second - self.created_at.second) + " seconds ago"
        if self.created_at.hour == time.hour:
            return str(time.minute - self.created_at.minute) + " mins ago"
        if self.created_at.day == time.day:
            return str(time.hour - self.created_at.hour) + " h"
        if self.created_at.month == time.month:
            return str(time.day - self.created_at.day) + " d"
        if self.created_at.year == time.year:
            return str(time.month - self.created_at.month) + " m"
        return self.created_at

class Posts(models.Model):

    def validate_file_extension(value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.png','.jpg','.jpeg']
        if not ext in valid_extensions:
            messages.error(value, 'File not supported')

    post_content = models.CharField(max_length=long_len)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    post_image = models.ImageField(upload_to='posts_pics', blank=True, null=True)
    tags = models.ManyToManyField(Tags)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like')
    comments = models.ManyToManyField('main.Comment', related_name='comments')
    shares = models.IntegerField(default=0)
    posted_at= models.DateTimeField(auto_now_add=True)

    favourites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')



class Comment(models.Model):
    comment_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    commented_at = models.DateTimeField(auto_now=True)
    comment_cont = models.TextField()
    post_to_comment = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=False)

class Answer(models.Model):
    ans_content = models.TextField()
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False)
    question_to_ans = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=False)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_a_upvote')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_a_downvote')
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)

class Vote(models.Model):
    post = models.ForeignKey(Questions, related_name='postid',
                             on_delete=models.CASCADE, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userid',
                             on_delete=models.CASCADE, default=None, blank=True)
    vote = models.BooleanField(default=True)

