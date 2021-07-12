from django.contrib import admin
from .models import Student, Teacher, User, Attendance
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
admin.site.register(Attendance)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(User, UserAdmin)