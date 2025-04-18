from django.contrib import admin
from django.utils.html import format_html
from .models import Event, EventCategory

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return format_html('<div style="width: 50px; height: 50px; background: #ccc; border-radius: 5px;"></div>')
    
    image_preview.short_description = 'Preview'

    list_display = ('image_preview', 'title', 'date', 'location', 'category', 'organizer', 'status', 'capacity')
    list_filter = ('status', 'category', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    filter_horizontal = ('attendees',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', ('image', 'image_preview'))
        }),
        ('Event Details', {
            'fields': ('date', 'location', 'category', 'capacity', 'registration_deadline')
        }),
        ('Status & Organization', {
            'fields': ('status', 'organizer', 'attendees')
        }),
        ('Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
