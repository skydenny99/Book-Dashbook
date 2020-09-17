from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_active',)
    list_filter = ('email', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_author', 'is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_author', 'is_active',
                       'first_name', 'last_name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    pass


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Comment)