from django.shortcuts import render

# Create your views here.


def main_home(request):
    return render(request, 'Books/main.html', {})
