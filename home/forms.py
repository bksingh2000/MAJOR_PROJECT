from django import forms 
from .models import Attendence, Student, Teacher, Attendance
# from django.contrib.auth.models import User

# class AttendenceForm(forms.ModelForm): 
#     class Meta: 
#         model = Attendence
#         fields = ['name', 'image']
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student','status']
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ()

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'bio', 'location', 'birth_date')

class StudentProfilePicForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('header_pic', 'profile_pic')

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'bio', 'location', 'birth_date')

class TeacherProfilePicForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('header_pic', 'profile_pic')