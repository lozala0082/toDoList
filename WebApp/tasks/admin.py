from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'due_date', 'status')
    list_filter = ('status', 'due_date', 'creator')
    search_fields = ('name', 'description')
    filter_horizontal = ('assignees',) 