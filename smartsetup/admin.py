from django.contrib import admin
from smartsetup.models import UserProfile
from django.utils.html import format_html

# Register your models here.

admin.site.site_header = 'SmartCount Administration'


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="40" style="border-radius:50px" />'.format(object.image.url))

    thumbnail.short_description = 'photo'
    list_display = ('id', 'thumbnail', 'user', 'job_description')
    list_display_links = ('thumbnail', 'user',)


admin.site.register(UserProfile, UserProfileAdmin)
