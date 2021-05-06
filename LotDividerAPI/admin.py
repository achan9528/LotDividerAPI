from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from LotDividerAPI.models import User

# registers the User model with the admin site
admin.site.register(User, UserAdmin)