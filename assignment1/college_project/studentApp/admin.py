from django.contrib import admin
from .models import Student, Department

admin.site.register(Department)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'age', 'roll_number', 'department']
    list_filter = ['department']
    search_fields = ['name', 'roll_number']
    ordering = ['name']