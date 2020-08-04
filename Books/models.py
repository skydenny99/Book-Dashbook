from idlelib.idle_test.test_run import S
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.conf import settings
from enum import Enum
from django.contrib.auth.models import BaseUserManager, AbstractUser

# Create your models here.
#fs = FileSystemStorage(location='/media/photos')
"""
class UserType(Enum):
    MANAGE = "Manager of service"
    AUTHOR = "Author of Book"
    NORMAL = "Normal user"


class User(AbstractUser):

    user_email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        primary_key=True
    )
    user_pw = models.CharField(max_length=50)
    user_nickname = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=32)
    user_job = models.CharField(max_length=20)
    registered_date = models.DateTimeField(
        auto_now_add=True
    )

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

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'user_email'
    REQUIRED_FIELDS = ['user_nickname', 'user_name', 'user_job']

    class Meta:
        indexes = [
            models.Index(fields=['user_right', 'user_email']),
        ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Must email')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
    pass


class User(AbstractUser): # from step 2
    ...
    objects = UserManager()
"""


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


