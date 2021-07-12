from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    @property
    def is_student(self):
        if hasattr(self, 'student'):
            return True
        return False

    @property
    def is_teacher(self):
        if hasattr(self, 'teacher'):
            return True
        return False

# class Class(models.Model):
#     section = models.CharField(max_length=100)

#     class Meta:
#         verbose_name_plural = 'classes'

#     def __str__(self):
#         return (self.section)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    # class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    header_pic = models.ImageField(upload_to='header', blank=True)
    profile_pic = models.ImageField(upload_to='profile', blank=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name
    


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    header_pic = models.ImageField(upload_to='header', blank=True)
    profile_pic = models.ImageField(upload_to='profile', blank=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name

# class Assign(models.Model):
#     class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
#     # course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = (('class_id', 'teacher'),)

    # def __str__(self):
    #     cl = Class.objects.get(id=self.class_id_id)
    #     te = Teacher.objects.get(id=self.teacher_id)
    #     return '%s : %s' % (te.first_name, cl)

# class AttendanceClass(models.Model):
#     assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.IntegerField(default=0)

#     class Meta:
#         verbose_name = 'Attendance'
#         verbose_name_plural = 'Attendance'

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # attendanceclass = models.ForeignKey(Assign, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.student)+" - "+str(self.date)
    

    # class Meta:
    #     unique_together = (('student','date'),)
    

# class Attendance(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     attendanceclass = models.ForeignKey(Assign, on_delete=models.CASCADE, default=1)
#     date = models.DateField(default='2018-10-23')
#     status = models.BooleanField(default='True')

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Attendence(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='')