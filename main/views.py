from django.shortcuts import render, redirect, get_object_or_404
from .models import Tags, Questions, Answer, Posts, Comment, Vote
from userauth.models import StackoverflowUser
from django.db import transaction
from django.db.models import Count, Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import reputation, performUpDownVote, performLike
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F
from django.db.models import Q
# Create your views here.

def reputation(booleanval, rate, ques_obj):
    if booleanval == False:
        userrepu = ques_obj.author
    else:
        userrepu = ques_obj.answered_by

    userrepu.reputation_score += rate
    userrepu.save()

def thumbs(request):

    if request.POST.get('action') == 'thumbs':

        id = int(request.POST.get('postid'))
        button = request.POST.get('button')
        update = Questions.objects.get(pk=id)
        flag=False

        if update.thumbs.filter(id=request.user.id).exists():
            # Get the users current vote (True/False)
            q = Vote.objects.get(
                Q(post_id=id) & Q(user_id=request.user.id))
            evote = q.vote

            if evote == True:

                # Now we need action based upon what button pressed
                if button == 'thumbsup':
                    reputation(flag,20, update)
                    update.thumbsup = F('thumbsup') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

                if button == 'thumbsdown':
                    # Change vote in Post
                    reputation(flag,-20, update)
                    update.thumbsup = F('thumbsup') - 1
                    update.thumbsdown = F('thumbsdown') + 1
                    update.save()

                    # Update Vote
                    q.vote = False
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

            pass

            if evote == False:

                if button == 'thumbsup':

                    # Change vote in Post
                    reputation(flag,20, update)
                    update.thumbsup = F('thumbsup') + 1
                    update.thumbsdown = F('thumbsdown') - 1
                    update.save()

                    # Update Vote
                    q.vote = True
                    q.save(update_fields=['vote'])

                    # Return updated votes
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    return JsonResponse({'up': up, 'down': down})

                if button == 'thumbsdown':

                    reputation(flag,-20, update)
                    update.thumbsdown = F('thumbsdown') - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()

                    return JsonResponse({'up': up, 'down': down, 'remove': 'none'})

        else:        # New selection

            if button == 'thumbsup':
                reputation(flag,20, update)
                update.thumbsup = F('thumbsup') + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                # Add vote down
                reputation(flag,-20, update)
                update.thumbsdown = F('thumbsdown') + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new vote
                new = Vote(post_id=id, user_id=request.user.id, vote=False)
                new.save()

            # Return updated votes
            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown

            return JsonResponse({'up': up, 'down': down})

    pass

def questions(request):
    main_query = Questions.objects
    if request.GET and ('q' in request.GET) and request.GET['q'] == 'mostviewed':
        all_questions = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and ('q' in request.GET) and request.GET['q'] == 'unanswered':
        all_questions = main_query.filter(
            is_answered=False).order_by('-created_at')
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_questions = main_query.all().order_by('-created_at')

    total_questions = Questions.objects.count()
    seeuser = StackoverflowUser

    user = request.user

    try:
        if request.GET and request.GET['isQuestion'] and request.GET['id'] and request.GET['action_type']:
            result = performUpDownVote(
                user, request.GET['isQuestion'], request.GET['id'], request.GET['action_type'])
            redirect_to = '/question/'+str(pk)
            if 'page' in request.GET:
                redirect_to += '?page='+request.GET['page']
            return redirect(redirect_to)
    except Exception:
        pass

    if request.method == 'POST':
        questiontaken = request.POST.dict()
        title = questiontaken.get('title')
        content = questiontaken.get('queseditor')
        tags = questiontaken.get('tags')
        selfanswer = questiontaken.get('selfanswereditor')

        q = Questions(title=title, ques_content=content, author=user)
        if selfanswer != '':
            q.is_answered = True
        q.save()
        all_tags = tags.split(',')

        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word=a)
                q.tags.add(t)
            except Exception:
                q.tags.create(tag_word=a)

            q.save()

        if selfanswer != '':
            a = Answer(ans_content=selfanswer,
                       answered_by=user, question_to_ans=q)
            a.is_accepted = True
            print(a)
            a.save()
            q.answers.add(a)
            q.has_accepted_answer = True

            q.save()
            user.ans_given.add(a)
        user.ques_asked.add(q)
        user.save()
        

        messages.success(request, 'Question posted successfully')

        return redirect('name_questionsingle', pk=q.pk)

    # Pagination
    #page = request.GET.get('page', 1)
    #paginator = Paginator(all_questions, 5)
    # try:
        #all_questions = paginator.page(page)
    # except EmptyPage:
    #     all_questions = paginator.page(paginator.num_pages)
    # except Exception as e:
        #all_questions = paginator.page(1)

    return render(request, 'main/questions1.html', {'all_questions': all_questions, 'marked': marked, 'total_questions': total_questions, 'seeuser': seeuser})

@login_required
def like(request):
    if request.POST.get('action') == 'POST':
        result = ''
        id = int(request.POST.get('id'))
        p = Posts.objects.get(pk=id)
        if p.likes.filter(id=request.user.id).exists():
            p.likes.remove(request.user)
            p.like_count -= 1
            result = p.like_count
            p.save()
        else:
            p.likes.add(request.user)
            p.like_count += 1
            result = p.like_count
            p.save()

        return JsonResponse({'result': result, })


@login_required
def askquestion(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        title = questiontaken.get('title')
        content = questiontaken.get('queseditor')
        tags = questiontaken.get('tags')
        selfanswer = questiontaken.get('selfanswereditor')

        q = Questions(title=title, ques_content=content, author=user)
        if selfanswer != '':
            q.is_answered = True
        q.save()
        all_tags = tags.split(',')

        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word=a)
                q.tags.add(t)
            except Exception:
                q.tags.create(tag_word=a)

            q.save()

        if selfanswer != '':
            a = Answer(ans_content=selfanswer,
                       answered_by=user, question_to_ans=q)
            a.is_accepted = True
            print(a)
            a.save()
            q.answers.add(a)
            q.has_accepted_answer = True

            q.save()
            user.ans_given.add(a)
        user.ques_asked.add(q)
        user.save()

        messages.success(request, 'Question posted successfully')

        return redirect('name_questionsingle', pk=q.pk)
    return render(request, 'Main:questions1.html')


def posts(request):
    main_query = Posts.objects
    if request.GET and ('p' in request.GET) and request.GET['p'] == 'mostviewed':
        all_posts = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and ('p' in request.GET) and request.GET['p'] == 'unanswered':
        all_posts = main_query.filter(is_answered=False).order_by('-posted_at')
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_posts = main_query.all().order_by('-posted_at')

    total_posts = Posts.objects.count()
    user = request.user
    del_post = Posts.objects
    is_author = True if user == del_post else False

    try:
        if request.GET and request.GET['isPost'] and request.GET['id'] and request.GET['action_type']:
            result = performLike(
                user, request.GET['isPost'], request.GET['id'], request.GET['action_type'])
            redirect_to = '/post/'+str(pk)
            if 'page' in request.GET:
                redirect_to += '?page='+request.GET['page']
            return redirect(redirect_to)
    except Exception:
        pass

    if request.method == 'POST':
        posttaken = request.POST.dict()
        content = posttaken.get('posteditor')
        tags = posttaken.get('tags')
        posts_image = request.FILES.get('fileInput')

        p = Posts(post_content=content, post_image=posts_image, author=user)
        p.save()

        all_tags = tags.split(',')

        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word=a)
                p.tags.add(t)
            except Exception:
                p.tags.create(tag_word=a)
            p.save()

        user.save()
        user.post_posted.add(p)

        messages.success(request, 'Posted successfully')
        return redirect('name_posts')

    return render(request, 'main/posts.html', {'del_post': del_post, 'is_author': is_author, 'all_posts': all_posts, marked: 'marked', 'total_posts': total_posts})


@login_required
def questionsingle(request, pk):
    # user = StackoverflowUser.objects.get(pk=1)
    user = request.user
    try:
        if request.GET and request.GET['isQuestion'] and request.GET['id'] and request.GET['action_type']:
            result = performUpDownVote(
                user, request.GET['isQuestion'], request.GET['id'], request.GET['action_type'])
            redirect_to = '/question/'+str(pk)
            if 'page' in request.GET:
                redirect_to += '?page='+request.GET['page']
            return redirect(redirect_to)
    except Exception:
        pass

    q = Questions.objects.get(pk=pk)
    if request.method == 'POST':
        questiontaken = request.POST.dict()
        answer = questiontaken.get('editor1')  # Answer content
        a = Answer(ans_content=answer, answered_by=user, question_to_ans=q)
        a.save()
        q.answers.add(a)
        messages.success(request, 'Answer posted successfully')
    q.views = q.views + 1
    q.save()

    if q.author == user:
        showaccept = True
    else:
        showaccept = False

    # Pagination
    all_answers = q.answers.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_answers, 5)
    try:
        all_answers = paginator.page(page)
    except PageNotAnInteger:
        all_answers = paginator.page(1)
    except EmptyPage:
        all_answers = paginator.page(paginator.num_pages)

    return render(request, 'main/question-details.html', {'q': q, 'all_answers': all_answers, 'showaccept': showaccept})


@login_required
def postdetail(request, pk):
    # user = StackoverflowUser.objects.get(pk=1)
    user = request.user
    try:
        if request.GET and request.GET['isPost'] and request.GET['id'] and request.GET['action_type']:
            result = performLike(
                user, request.GET['isPost'], request.GET['id'], request.GET['action_type'])
            redirect_to = '/post/'+str(pk)
            if 'page' in request.GET:
                redirect_to += '?page='+request.GET['page']
            return redirect(redirect_to)
    except Exception:
        pass

    p = Posts.objects.get(pk=pk)
    if request.method == 'POST':
        commentstaken = request.POST.dict()
        comment = commentstaken.get('comment')  # Answer content
        c = Comment(comment_cont=comment, comment_by=user, post_to_comment=p)
        c.save()
        p.comments.add(c)
        messages.success(request, 'Comment posted')
    p.shares = p.shares + 1
    p.save()

    all_comments = p.comments.all()

    return render(request, 'main/post-details.html', {'p': p, 'all_comments': all_comments})


@login_required
def delete_post(request, id):
    post_to_delete = Posts.objects.get(id=id)
    user = request.user
    p = post_to_delete.author
    show_del_button = True if user == p else False
    post_to_delete.delete()
    messages.info(request, "Post deleted successfully!")
    return redirect("/posts/", {'p': p, 'post_to_delete': post_to_delete, 'show_del_button': show_del_button})


@login_required
def delete_quest(request, id):
    quest_to_delete = Questions.objects.get(id=id)
    user = request.user
    q = quest_to_delete.author
    show_del_button = True if user == q else False
    quest_to_delete.delete()
    messages.info(request, "Question deleted successfully!")
    return redirect("/", {'q': q, 'quest_to_delete': quest_to_delete, 'show_del_button': show_del_button})

@login_required
def delete_answer(request, id):
    ans_to_delete = Answer.objects.get(id=id)
    user = request.user
    a = ans_to_delete.answered_by
    show_del_button = True if user == a else False
    ans_to_delete.delete()
    messages.info(request, "Answer deleted successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'a': a, 'ans_to_delete': ans_to_delete, 'show_del_button': show_del_button})


@login_required
def delete_comment(request, id):
    comment_to_delete = Comment.objects.get(id=id)
    user = request.user
    c = comment_to_delete.comment_by
    show_del_button = True if user == c else False
    comment_to_delete.delete()
    messages.info(request, "Comment deleted successfully!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'c': c, 'comment_to_delete': comment_to_delete, 'show_del_button': show_del_button})


@login_required
def createpost(request):
    user = request.user
    print(user)
    if request.method == 'POST':
        posttaken = request.POST.dict()
        content = posttaken.get('posteditor')
        tags = posttaken.get('tags')
        posts_image = request.FILES.get('fileInput')

        p = Posts(post_content=content, post_image=posts_image, author=user)
        p.save()

        all_tags = tags.split(',')

        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word=a)
                p.tags.add(t)
            except Exception:
                p.tags.create(tag_word=a)
            p.save()

        user.save()
        user.post_posted.add(p)

        messages.success(request, 'Posted successfully')
        return redirect('name_posts')
    return render(request, 'main/create-post.html')


def questionByTag(request, tag_word):
    main_query = Questions.objects.filter(Q(tags__tag_word__iexact=tag_word))

    if request.GET and request.GET['q'] == 'mostviewed':
        all_questions = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and request.GET['q'] == 'unanswered':
        all_questions = main_query.filter(is_answered=False)
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_questions = main_query.all().order_by('-created_at')

    return render(request, 'main/questions1.html', {'all_questions': all_questions, 'marked': marked})


def postByTag(request, tag_word):
    main_query = Posts.objects.filter(Q(tags__tag_word__iexact=tag_word))

    if request.GET and request.GET['p'] == 'mostviewed':
        all_posts = main_query.all().order_by('-views')
        marked = 'mostviewed'
    elif request.GET and request.GET['p'] == 'unanswered':
        all_posts = main_query.filter(is_answered=False)
        marked = 'unanswered'
    else:
        marked = 'latest'
        all_posts = main_query.all().order_by('-posted_at')

    return render(request, 'main/posts.html', {'all_posts': all_posts, 'marked': marked})

@login_required
def delete_account(request):   
    user = request.user
    user.delete()
    messages.success(request, "Account deleted successfully")          

    return redirect(request, 'name_questions') 

@login_required
def profile(request, username):
    seeuser = StackoverflowUser.objects.get(username=username)
    showeditbutton = True if seeuser == request.user else False
    showDeleteButton = True if seeuser == request.user else False 
    userques = Questions.objects.filter(author=seeuser).order_by('-created_at')
    userposts = Posts.objects.filter(author=seeuser).order_by('-posted_at')
    ansgiven = Answer.objects.filter(
        answered_by=seeuser).order_by('-created_at')
    uservotes = Questions.objects.filter(
        author=seeuser).order_by('-created_at')

    user = request.user

    if request.method == 'POST':
        questiontaken = request.POST.dict()
        title = questiontaken.get('title')
        content = questiontaken.get('queseditor')
        tags = questiontaken.get('tags')
        selfanswer = questiontaken.get('selfanswereditor')

        q = Questions(title=title, ques_content=content, author=user)
        if selfanswer != '':
            q.is_answered = True
        q.save()
        all_tags = tags.split(',')

        for a in all_tags:
            try:
                t = Tags.objects.get(tag_word=a)
                q.tags.add(t)
            except Exception:
                q.tags.create(tag_word=a)

            q.save()

        if selfanswer != '':
            a = Answer(ans_content=selfanswer,
                       answered_by=user, question_to_ans=q)
            a.is_accepted = True
            print(a)
            a.save()
            q.answers.add(a)
            q.has_accepted_answer = True

            q.save()
            user.ans_given.add(a)
        user.ques_asked.add(q)
        user.save()

        messages.success(request, 'Question posted successfully')

        return redirect('name_questionsingle', pk=q.pk)

    return render(request, 'main/profile.html', {'seeuser': seeuser, 'showeditbutton': showeditbutton, 'userques': userques,'userposts':userposts, 'ansgiven': ansgiven, 'uservotes': uservotes})



@login_required
def is_accepted(request, pk, pk2):
    q = Questions.objects.get(pk=pk)
    a = Answer.objects.get(pk=pk2)

    q.has_accepted_answer = True
    q.save()

    a.is_accepted = True
    a.save()

    if q.author == request.user:
        showaccept = True
    else:
        showaccept = False

    # Pagination
    all_answers = q.answers.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_answers, 5)
    try:
        all_answers = paginator.page(page)
    except PageNotAnInteger:
        all_answers = paginator.page(1)
    except EmptyPage:
        all_answers = paginator.page(paginator.num_pages)

    return render(request, 'main/question-details.html', {'q': q, 'all_answers': all_answers, 'showaccept': showaccept})
