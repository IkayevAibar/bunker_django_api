from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

class PlayerAdmin(UserAdmin):
    # autocomplete_fields=["school_id"]
    list_display = ('id','username','is_online','last_login','date_joined')
    list_display_links = ('username', 'id')
    fieldsets = (
        (None, {'fields': ('username','password', 'avatar','is_online')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser','last_login','date_joined')
        })
    )
    # inlines = [CourseInline,]

admin.site.register(User,PlayerAdmin)

# Register your models here.
