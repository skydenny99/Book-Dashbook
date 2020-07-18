from idlelib.idle_test.test_run import S

from django.db import models
from django.utils import timezone
from enum import Enum

# Create your models here.


class SeparatedValuesField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value):
        if not value: return
        assert(isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([str(s, 'utf-8') for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    created_date = models.DateTimeField(
        default=timezone.now(), auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        default=timezone.now(), auto_now=True
    )

    book_name = models.CharField(max_length=20)
    book_hash_tags = SeparatedValuesField()
    book_author = models.CharField(max_length=50)
    book_info = models.TextField()
    book_image_url = models.TextField()

    def create(self):
        self.created_date = timezone.now()
        self.last_updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.book_id + ':' + self.book_name


class Chapter(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    chapter_num = models.IntegerField()
    chapter_name = models.CharField(max_length=20)
    chapter_info = models.TextField()
    chapter_hash_tags = SeparatedValuesField()
    chapter_subs = SeparatedValuesField()
    chapter_threads_count = models.IntegerField(
        default=0
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'chapter_num'], name='unique_book_chapter')
        ]
        indexes = [
            models.Index(fields=['book_id', 'chapter_num']),
            models.Index(fields=['book_id'], name='book_idx'),
        ]

    def create(self):
        self.chapter_threads_count = 0
        self.save()

    def __str__(self):
        return self.book_id + ':' + self.chapter_id + ':' + self.chapter_name


class ThreadState(Enum):
    AUTHOR_HELPED = "Author contributed"
    KEEP_GOING = "Discussion keep going"
    ANSWERED = "Answered"


class Thread(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    thread_id = SeparatedValuesField()
    thread_name = models.CharField(max_length=30)
    thread_writer = models.ForeignKey('User', on_delete=models.CASCADE) # 유저 탈퇴시 모든 작성 내용 삭제?
    thread_hash_tags = SeparatedValuesField()
    thread_count = models.IntegerField(
        default=1
    )
    thread_contrib_count = models.IntegerField(
        default=1
    )
    thread_likes = models.IntegerField(
        default=0
    )
    thread_visits = models.IntegerField(
        default=0
    )
    thread_states = SeparatedValuesField()
    created_date = models.DateTimeField(
        default=timezone.now(), auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        default=timezone.now(), auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'thread_id'], name='unique_book_thread')
        ]
        indexes = [
            models.Index(fields=['book_id', 'thread_id']),
            models.Index(fields=['book_id'], name='book_idx'),
        ]


    def create(self):
        self.thread_count = 1
        self.thread_contrib_count = 1
        self.thread_likes = 0
        self.thread_visits = 0
        self.created_date = timezone.now()
        self.last_updated_date = timezone.now()
        self.save()


class Post(models.Model):
    book_id = models.ForeignKey('Book', on_delete=models.CASCADE)
    post_id = SeparatedValuesField()
    post_writer = models.ForeignKey('User', on_delete=models.CASCADE) # 유저 탈퇴시 모든 작성 내용 삭제?
    created_date = models.DateTimeField(
        default=timezone.now(), auto_now_add=True
    )
    last_updated_date = models.DateTimeField(
        default=timezone.now(), auto_now=True
    )
    post_content = models.TextField()
    post_likes = models.IntegerField(
        default=0
    )
    post_adopted = models.BooleanField(
        default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book_id', 'post_id'], name='unique_book_post')
        ]
        indexes = [
            models.Index(fields=['book_id', 'post_id']),
            models.Index(fields=['book_id'], name='book_idx'),
        ]

    def create(self):
        self.post_likes = 0
        self.post_adopted = False
        self.created_date = timezone.now()
        self.last_updated_date = timezone.now()
        self.save()


"""
class UserJob(Enum):
    AUTHOR_HELPED = "Author contributed"
    KEEP_GOING = "Discussion keep going"
    ANSWERED = "Answered"
"""


class UserType(Enum):
    MANAGE = "Manager of service"
    AUTHOR = "Author of Book"
    NORMAL = "Normal user"


class User(models.Model):
    user = models.IntegerField(primary_key=True)
    registered_date = models.DateTimeField(
        default=timezone.now(), auto_now_add=True
    )
    user_id = models.CharField(max_length=20)
    user_pw = models.CharField(max_length=32)
    user_nickname = models.CharField(max_length=20)
    user_name = models.CharField(max_length=32)
    user_job = models.CharField(max_length=20)
    user_email = models.CharField(max_length=100)
    user_info = models.TextField(
        blank=True, null=True
    )
    user_rank = models.IntegerField(
        default=1
    )
    user_right = models.CharField(
        max_length=6,
        choices=[(tag, tag.value) for tag in UserType]  # Choices is a list of Tuple
    )
    user_attention = SeparatedValuesField()
    user_career = SeparatedValuesField()
    user_history = SeparatedValuesField()
    user_subscribe = SeparatedValuesField()
    # 해쉬태그별 TOP4, 유저 작성 쓰레드 수

    def create(self):
        user_rank = 1
        
        self.save()

    def modify(self):
        self.save()

    pass
