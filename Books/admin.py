from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

# admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Comment)