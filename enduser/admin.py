from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Announcement)
admin.site.register(Landing)
admin.site.register(Category)
admin.site.register(Subject)
admin.site.register(Why)
admin.site.register(Team)

class AnnouncementBarAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Disable add permission if there's already an instance
        return not AnnouncementBar.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission
        return False

admin.site.register(AnnouncementBar, AnnouncementBarAdmin)