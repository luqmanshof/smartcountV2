from django.contrib import admin

# Register your models here.
from smartsetup.models import UserProfile

admin.site.site_header = 'SmartCount Administration'
admin.site.register(UserProfile)
