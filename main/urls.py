from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.questions, name = 'name_questions'),
    path('tag/<str:tag_word>/', views.questionByTag, name = 'name_questionByTag'),
    path('tag/<str:tag_word>/', views.postByTag, name = 'name_postByTag'),
    path('question/<int:pk>/', views.questionsingle, name = 'name_questionsingle'),
    path('post/<int:pk>/', views.postdetail, name = 'name_postdetail'),
    path('askquestion/', views.askquestion, name = 'name_askquestion'),
    path('createpost/', views.createpost, name = 'name_createpost'),
    path('posts/', views.posts, name = 'name_posts'),
    path('profile/<str:username>/', views.profile, name = 'name_profile'),
    path('question/<int:pk>/<int:pk2>/', views.is_accepted, name = 'name_is_accepted'),
    path('post_deleted/<int:id>', views.delete_post, name = 'post_deleted'),
    path('question_deleted/<int:id>', views.delete_quest, name = 'question_deleted'),
    path('comment_deleted/<int:id>', views.delete_comment, name = 'comment_deleted'),
    path('thumbs/', views.thumbs, name='thumbs'),
    path('like/', views.like, name='like'),
]


if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)