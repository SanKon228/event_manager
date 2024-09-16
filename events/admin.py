from django.contrib import admin
from .models import Event, Attendee

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'organizer')
    search_fields = ('title', 'description')
    list_filter = ('date', 'location')
    ordering = ('date',)

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'date_registered')
    search_fields = ('user__username', 'event__title')
    list_filter = ('date_registered',)
