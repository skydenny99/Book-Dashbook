from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import *
# Create your views here.


def main_home(request):
    return render(request, 'Books/main.html', {})


def thread_new(request):
    user = request.user
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.thread_writer = user
            print(request.path_info)
            thread.thread_id = 'request.path_info' + str(thread.id)
            thread.save()
            return render_to_response('Books/thread.html', RequestContext(request))
    else:
        form = ThreadForm()
    return render(request, 'Books/thread_write.html', {'form':form})

def post_new(request):
    form = PostForm()
    return render(request, 'Books/thread_write.html', {'form':form})