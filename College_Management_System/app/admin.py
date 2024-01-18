from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from .models import CustomUser, Department

# Register your models here.

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'phone_number', 'address', 'department_id', 'pic')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type', 'phone_number', 'address', 'department_id', 'pic')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'phone_number', 'address', 'department_id')

    fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal Info', {'fields': ('email', 'user_type', 'phone_number', 'address', 'department_id', 'pic')}),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'user_type', 'phone_number', 'address', 'department_id', 'pic'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_filter = ['user_type']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Department)

admin.site.unregister(Group)
admin.site.site_header = 'COLLEGE MANAGEMENT SYSTEM'
