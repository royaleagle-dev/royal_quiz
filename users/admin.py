from django.contrib import admin

# Register your models here.

from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'RP', 'date_of_birth', 'status')
admin.site.register(Profile, ProfileAdmin)
