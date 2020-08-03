from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_home, name='main_home'),
    #path('books/<int:pk>/', views.chapter_show, name='chapter_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/', views.chapter_show, name='chapter_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/', views.thread_show, name='thread_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread-write/', views.thread_new, name='thread_new'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/post-new', views.post_new, name='post_new'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/comment-new', views.comment_new, name='comment_new'),
]