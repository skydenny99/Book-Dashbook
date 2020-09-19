from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title', 'book_author', 'book_info', 'book_hash_tags']

class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['thread_title', 'thread_text', 'thread_hash_tags']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_text']

class ThreadEditForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['thread_text']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text']

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_author', 'user_info']
    pass

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_author', 'user_info']
    pass