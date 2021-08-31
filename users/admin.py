from django.contrib import admin
from .models import User, Trader, TraderDocument
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'fullname', 'user_role')
    list_filter = ('user_role',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('fullname', 'address', 'contact', 'joined_date', 'is_active')}),
        ('Token info', {'fields': ('otp', 'otp_last_date')}),
        ('Permissions', {'fields': ('user_role',)}),
    )
    readonly_fields=('joined_date',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.register(Trader)
admin.site.register(TraderDocument)