from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from .forms import *
from .models import *
# Create your views here.


def main_home(request):
    return render(request, 'Books/main.html', {})


def book_show(request):
    chapters = Chapter.objects.filter(book_id__exact=Book.objects.get(pk=request.POST.get('book_id'))).order_by('chapter_num')
    return render(request, 'Books/book.html', {'chapters':chapters})


def chapter_show(request, book_id=None, chapter_num=None):
    book = Book.objects.get(pk=book_id)
    chapter = Chapter.objects.filter(book_id=book).get(chapter_num=chapter_num)
    threads = Thread.objects.filter(book_id__exact=book).filter(chapter_id__exact=chapter).order_by('-created_date')
    return render(request, 'Books/chapter.html', {'book_id':book_id, 'threads':threads, 'chapter_num':chapter_num})


def thread_show(request, book_id=None, chapter_num=None, thread_id=None):
    thread = get_object_or_404(Thread, id=thread_id)
    if not request.session.get('viewed_thread_%s' % thread_id, None): # 시스템 부하걸릴 수 있음 -> google analystic이나 statD사용
        request.session['viewed_thread_%s' % thread_id] = True
        thread.thread_views += 1
        thread.save()

    posts = Post.objects.filter(book_id__exact=Book.objects.get(pk=book_id)).\
        filter(thread_id__exact=Thread.objects.get(pk=thread_id)).order_by('created_date')
    thread.thread_count = len(posts)
    comments = Comment.objects.filter(book_id__exact=Book.objects.get(pk=book_id)).\
        filter(thread_id__exact=Thread.objects.get(pk=thread_id))
    return render(request, 'Books/thread.html', {'thread':thread, 'posts':posts, 'chapter_num':chapter_num, 'comments':comments})


def thread_new(request, book_id=None, chapter_num=None):
    user = auth.authenticate(username='admin', password='hcidusrntlf')
    # user = request.user
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.book_id = Book.objects.get(pk=book_id) # pk값 (book_id) url에서 받아오기 = form에서 hidden form element로 보내기(보안)
            thread.chapter_id = Chapter.objects.filter(book_id=thread.book_id).get(chapter_num=chapter_num)
            thread.thread_writer = user

            thread.save()
            return redirect('thread_show', book_id=book_id, chapter_num=chapter_num, thread_id=thread.id)
    else:
        form = ThreadForm()
    return render(request, 'Books/thread_write.html', {'form':form})


def post_new(request, book_id=None, chapter_num=None, thread_id=None):
    user = auth.authenticate(username='admin', password='hcidusrntlf')
    # user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.book_id = Book.objects.get(pk=book_id)  # pk값 (book_id) url에서 받아오기
            thread = Thread.objects.get(pk=thread_id)
            post.thread_id = thread
            # thread = Thread.objects.get(request.POST['id'])
            post.post_writer = user
            post.save()
            return redirect('thread_show', book_id=book_id, chapter_num=chapter_num, thread_id=thread_id)
    else:
        form = PostForm()
    return render(request, 'Books/thread.html', {'form':form})


def comment_new(request, book_id, chapter_num=None, thread_id=None, post_id=None):
    user = auth.authenticate(username='admin', password='hcidusrntlf')
    # user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book_id = Book.objects.get(pk=book_id)
            comment.thread_id = Thread.objects.get(pk=thread_id)
            comment.post_id = Post.objects.get(pk=post_id)
            # thread = Thread.objects.get(request.POST['id'])
            comment.comment_writer = user
            comment.save()
            return redirect('thread_show', book_id=book_id, chapter_num=chapter_num, thread_id=thread_id)
    return render(request, 'Books/thread.html', {})


def sign_up(request):
    pass


def login(request):
    pass


def logout(request):
    pass
