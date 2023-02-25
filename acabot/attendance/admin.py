from django.contrib import admin
from attendance.models import Attendance_Student

class AttendanceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Attendance_Student,AttendanceAdmin)
# Register your models here.
