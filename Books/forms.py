from django import forms

from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_title', 'book_author', 'book_info', 'book_hash_tags']

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_num', 'chapter_title', 'chapter_subs']

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
