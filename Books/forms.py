from django import forms

from .models import *


class ThreadForm(forms.ModelForm):

    class Meta:
        model = Thread
        fields = ['thread_title', 'thread_text', 'thread_hash_tags']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_text']

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text']
