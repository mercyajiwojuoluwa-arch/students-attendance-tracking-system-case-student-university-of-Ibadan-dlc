from django.contrib import admin
from .models import Student,Course,Session,Attendance
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
 list_display=('matric_no','full_name','email');search_fields=('matric_no','full_name')
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
 list_display=('code','title','lecturer');filter_horizontal=('students',)
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
 list_display=('course','date','topic');list_filter=('course','date')
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
 list_display=('session','student','present','recorded_at');list_filter=('present','session__course')
