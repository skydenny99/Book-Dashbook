from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main_home, name='main_home'),
    path('login_view', views.login_view, name='book_login_view'),
    path('books/<int:book_id>/', views.book_show, name='book_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/', views.chapter_show, name='chapter_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/', views.thread_show, name='thread_show'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread-write/', views.thread_new, name='thread_new'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/post-new', views.post_new, name='post_new'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/thread-edit', views.thread_edit, name='thread_edit'),
    path('books/<int:book_id>/chapter/<int:chapter_num>/thread/<int:thread_id>/comment-new', views.comment_new, name='comment_new'),
    path('book-new', views.book_new, name='book_new'),
    path('book-new/<int:chapter_count>', views.book_new, name='book_new'),
    path('login', views.login_user, name='book_login'),
    path('logout', views.logout_user, name='book_logout')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)