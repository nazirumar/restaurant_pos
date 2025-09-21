from django.contrib import admin
from .models import Employee, Shift


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'tenant', 'role', 'phone', 'hire_date')
    list_filter = ('role', 'tenant')
    search_fields = ('user__username', 'user__email', 'phone')
    ordering = ('tenant', 'user__username')


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_time', 'end_time', 'short_notes')
    list_filter = ('employee__tenant', 'start_time')
    search_fields = ('employee__user__username', 'notes')
    ordering = ('-start_time',)

    def short_notes(self, obj):
        return (obj.notes[:50] + '...') if len(obj.notes) > 50 else obj.notes
    short_notes.short_description = 'Notes'
