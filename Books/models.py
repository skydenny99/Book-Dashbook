from idlelib.idle_test.test_run import S
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.conf import settings
from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.
#fs = FileSystemStorage(location='/media/photos')

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    user_info = models.TextField(null=True, blank=True)
    user_rank = models.IntegerField(default=1)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()
    def __str__(self):
        return self.username

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        auto_now=True
    )

    book_title = models.CharField(max_length=20)
    book_hash_tags = models.TextField()
    book_author = models.CharField(max_length=50)
    book_info = models.TextField()
    book_image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['book_id']),
        ]

    def get_hash_tag(self):
        return self.book_hash_tags.split(',,')

    def __str__(self):
        return str(self.book_id) + ':' + self.book_title


class Chapter(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_num = models.IntegerField()
    chapter_title = models.CharField(max_length=20)
    chapter_info = models.TextField(null=True, blank=True)
    chapter_hash_tags = models.TextField()
    chapter_subs = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'chapter_num'], name='unique_book_chapter')
        ]
        indexes = [
            models.Index(fields=['book_id', 'chapter_num']),
        ]

    def chapter_contrib_count(self):
        threads = Thread.objects.filter(book_id=self.book_id).filter(chapter_id=self)
        count = 0
        for thread in threads:
            count += thread.thread_contrib_count
        return count

    def chapter_thread_count(self):
        return len(Thread.objects.filter(book_id=self.book_id).filter(chapter_id=self))

    def get_chapter_subs(self):
        return self.chapter_subs.split(',,')

    def get_hash_tag(self):
        return self.chapter_hash_tags.split(',,')

    def __str__(self):
        return str(self.book_id) + ':' + str(self.id) + ':' + self.chapter_title


class ThreadState(Enum):
    AUTHOR_HELPED = "Author contributed"
    KEEP_GOING = "Discussion keep going"
    ANSWERED = "Answered"


class Thread(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_id = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    thread_title = models.CharField(max_length=50)
    thread_text = models.TextField()
    thread_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저 탈퇴시 모든 작성 내용 삭제?
    # thread_writer = models.CharField(max_length=30)
    thread_hash_tags = models.TextField()
    thread_count = models.IntegerField(
        default=0
    )
    thread_contrib_count = models.IntegerField(
        default=1
    )
    thread_likes = models.IntegerField(
        default=0
    )
    thread_views = models.IntegerField(
        default=0
    )
    thread_states = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'id'], name='unique_book_thread')
        ]
        indexes = [
            models.Index(fields=['book_id', 'chapter_id', 'id']),
        ]

    def get_hash_tag(self):
        return self.thread_hash_tags.split(',,')

    def __str__(self):
        return str(self.book_id) + ':' + str(self.id) + ':' + self.thread_title


class Post(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    thread_id = models.ForeignKey('Thread', on_delete=models.CASCADE)
    post_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저 탈퇴시 모든 작성 내용 삭제?
    # post_writer = models.CharField(max_length=30)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        auto_now=True
    )
    post_text = models.TextField()
    post_likes = models.IntegerField(
        default=0
    )
    post_adopted = models.BooleanField(
        default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'id'], name='unique_book_post')
        ]
        indexes = [
            models.Index(fields=['book_id', 'thread_id', 'id']),
        ]

    def __str__(self):
        return str(self.thread_id) + ':' + str(self.id)


class Comment(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    thread_id = models.ForeignKey('Thread', on_delete=models.CASCADE)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, blank=True)
    comment_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 유저 탈퇴시 모든 작성 내용 삭제?
    # post_writer = models.CharField(max_length=30)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        auto_now=True
    )
    comment_text = models.CharField(max_length=255)
    pass


"""
class UserJob(Enum):
    AUTHOR_HELPED = "Author contributed"
    KEEP_GOING = "Discussion keep going"
    ANSWERED = "Answered"
"""


