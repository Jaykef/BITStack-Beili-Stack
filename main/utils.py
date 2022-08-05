from .models import Tags, Questions, Answer, Posts
from django.db.models import Count,Q
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages

# ©️ 2022 Jaykef | Jaward

def reputation(booleanval, rate, ques_obj):
    if booleanval == False:
        userrepu = ques_obj.author
    else:
        userrepu = ques_obj.answered_by

    userrepu.reputation_score += rate
    userrepu.save()

def performUpDownVote(user,isQuestion,id,action_type):
    id = int(id)
    flag = False
    if isQuestion == 'True':
        print('------> isQ')
        q = Questions.objects.get(pk = id)
        if q.author == user:
            return False
    else:
        print('------> isNotQ')
        flag=True
        q = Answer.objects.get(pk = id)
        if q.answered_by == user:
            return False

    existsInUpvote = True if user in q.upvotes.all() else False
    existsDownUpvote = True if user in q.downvotes.all() else False
    if existsInUpvote:
        if action_type == 'downvote':
            q.upvotes.remove(user)
            q.downvotes.add(user)
            reputation(flag,-20, q)
            q.votes = q.votes - 1
    elif existsDownUpvote:
        if action_type == 'upvote':
            q.downvotes.remove(user)
            q.upvotes.add(user)
            reputation(flag,20, q)
            q.votes = q.votes + 1
    else:
        if action_type == 'downvote':
            q.downvotes.add(user)
            reputation(flag,-10, q)
            q.votes = q.votes - 1
        if action_type == 'upvote':
            q.upvotes.add(user)
            reputation(flag,10, q)
            q.votes = q.votes + 1
    q.save()
    return True

def performLike(user,isPost,id,action_type):
    id = int(id)
    if isPost == 'True':
        print('------> isQ')
        p = Posts.objects.get(pk = id)
    else:
        print('------> isNotQ')
        q = Answer.objects.get(pk = id)

    existsInLike = True if user in p.likes.all() else False
    existsInUnlike = True if user in p.likes.all() else False
    if existsInLike:
        if action_type == 'unlike':
            p.likes.remove(user)
            p.likes = p.likes - 1
    elif existsInUnlike:
        if action_type == 'like':
            p.likes.add(user)
            p.likes = p.likes + 1
    else:
        if action_type == 'unlike':
            q.likes.add(user)
            p.likes = p.likes - 1
        if action_type == 'like':
            p.likes.add(user)
            p.likes = p.likes + 1
    p.save()
    return True

