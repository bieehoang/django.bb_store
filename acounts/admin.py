from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
# Create super admin to manage 
class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username', 'first_name', 'last_name') # fields have link attribute with site
    readonly_field = ('last_login', 'date_joined') 
    ordering = ('-date_joined',) # sort to begin

    # Must required when declared
    filter_horizontal = ()
    list_filter = ()
    fieldsets = () 

admin.site.register(Account, AccountAdmin)
