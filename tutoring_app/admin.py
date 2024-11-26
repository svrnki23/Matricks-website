from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Staffs, Students, Subjects, Courses, Attendance, AttendanceReport, FeedBackStudent, NotificationStaffs, NotificationStudent

# Register your models here.
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Staffs)
admin.site.register(Students)
admin.site.register(Subjects)
admin.site.register(Courses)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(FeedBackStudent)
admin.site.register(NotificationStaffs)
admin.site.register(NotificationStudent)


