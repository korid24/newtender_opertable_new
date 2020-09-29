from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(UserAdmin):
    '''
    Create and edit a user in the admin panel
    '''
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        ('Основная ийнформация', {'fields': ('email', 'password', 'first_name',
                                  'last_name', 'telegram_id')}),
        ('Права', {'fields': ('is_staff', 'is_active', 'is_superuser',
                              'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'is_staff', 'is_active', 'is_superuser')}
         ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
