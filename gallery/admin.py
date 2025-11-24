from django.contrib import admin
from .models import EventPhoto

@admin.register(EventPhoto)
class EventPhotoAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'uploaded_at')
    list_filter = ('event', 'uploaded_at')
    search_fields = ('caption', 'event__title')
    readonly_fields = ('uploaded_at',)
