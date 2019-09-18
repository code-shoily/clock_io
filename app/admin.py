from django.contrib import admin

from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time', 'duration', 'is_current')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    list_filter = ('user',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def is_current(self, obj):
        return obj.is_current
    is_current.admin_order_field = 'is_current'
    is_current.boolean = True

    def start_time(self, obj):
        return obj.start_time
    start_time.admin_order_field = 'start_time'

    def end_time(self, obj):
        return obj.end_time
    end_time.admin_order_field = 'end_time'

    def duration(self, obj):
        return obj.duration
    duration.admin_order_field = 'duration'
