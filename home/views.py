from django.shortcuts import render, redirect
from .models import Student, Attendance, Teacher
from .forms import AttendanceForm, StudentProfileForm, StudentProfilePicForm, TeacherProfileForm, TeacherProfilePicForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import face_recognition
import os, re
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import Http404
import datetime
from django.db import IntegrityError
from django.core.files.storage import FileSystemStorage 
import os
from django.db.models import Q

path = 'media/train/'
images = []
classNames = []
myLists = os.listdir(path)

for cl in myLists:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)

def faceRecognize(img):
    imgS = face_recognition.load_image_file(img)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    names = []
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            names.append(name)
    return names

# def index(request):
#     if request.method == 'POST':
#         form = AttendenceForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             img_obj = form.instance
#             query = form.cleaned_data['image']
#             name = faceRecognize(query)
#             return render(request, 'index.html', {'form': form, 'img_obj': img_obj, 'names':name})
#     else:
#         form = AttendenceForm()
#     return render(request, 'index.html', {'form': form})
@login_required
def index(request):
    return render(request,"main.html")

def page(request):
    return render(request,"page.html")

def saveTest(request):
    if request.method =='POST':
        # deleteOnRe()

        # Register user
        # all_students = []
        date = request.POST.get("date")
        students = request.POST.getlist("student")
        for student in students:
            s = Attendance.objects.get(student__pk=student,date=date)
            s.status=True
            s.save()
            # mark_absent, c = Attendance.objects.get_or_create(student__pk=student, date=date,status=True)
            # if c:
            #     pass
            # else:
            #     pass
        
        # all_student = Student.objects.all()
        # print((all_student))
        # for all_stu in all_student:
        #     present = Attendance.objects.get(student=all_stu.)
        return redirect('confirm')
    else:
        pass
        # return render(request,'accounts/register.html')

@login_required
def take_attendence(request):
    if request.user.is_teacher:
        students = []
        # e = ""
        attendees = []
        if request.method == 'POST':
            deleteOnRe()
            all_student = Student.objects.all()
        # print((all_student))
            for all_stu in all_student:
                mark_absent, c = Attendance.objects.get_or_create(student=all_stu, date=datetime.datetime.now().strftime("%Y-%m-%d"),status=False)
                if c:
                    pass
                else:
                    pass
            query = request.FILES['image']
            name = faceRecognize(query)
            # print(name)
            for n in name:
                # absent_student = Student.objects.filter(~Q(first_name=n))
                s = Student.objects.get(first_name__iexact=n)
                # print(s)
                stu = Student.objects.filter(first_name__iexact=n)
                students.append(stu)
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                ins, cre = Attendance.objects.update_or_create(student=s,date=date, defaults={'status': 'True'})
                if cre:
                    pass
                else:
                    pass

                # ins, cre = Attendance.objects.get_or_create(student=absent_student, date=date, status=False)
                # if cre:
                #     pass
                # else:
                #     pass
            #     attendees.append(Attendance(student=s, date=date, status=True))
                
            # Attendance.objects.bulk_create(attendees)

                    # return render(request, 'mark.html', {'names':'dummy', 'students':students, 'error':e})
            # print(students)

            # markAttendence("Badal")

            return render(request, 'mark.html', {'names':'dummy', 'students':students})
        return render(request, 'mark.html') 
    else:
        raise Http404
# def markAttendance(student):
#     students = Student.objects.all()
#     attendance = Attendance.objects

def markAttendence(name):
    student_name = Student.objects.get(first_name=name)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    attend = Attendance(student=student_name, date=date, status=True)
    attend.save()

def deleteOnRe():
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    attend = Attendance.objects.filter(date=date).delete()

@login_required
def show_attendence(request):
    if request.user.is_student:
        view = Attendance.objects.filter(student=request.user.student).order_by('-date')
        return render(request, 'show.html', {'views':view})
        # return render(request, 'show.html')
    else:
        raise Http404

class MyFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if os.path.exists(self.path(name)):
            os.remove(self.path(name))
        return name

@login_required
@csrf_exempt
def train(request):
    msg=""
    if request.method == 'POST' and request.FILES['image']:
        myfile = request.FILES['image']
        fs = MyFileSystemStorage(location=path)
        filename = request.user.student.first_name+".jpg"
        # print(filename)
        filesave = fs.save(filename, myfile)
        msg = "Trained!!"
    return render(request, 'data.html', {'msg':msg})

@login_required
@csrf_exempt
def camtrain(request):
    if request.method == 'POST' and request.POST['img']:
        imgdata = base64.b64decode(re.search(r'base64,(.*)', request.POST['img']).group(1))
        filename = request.user.student.first_name+".jpg"  # I assume you have a way of picking unique filenames
        # print(filename)
        with open(path+"/"+filename, 'wb') as f:
            f.write(imgdata)

        return HttpResponse("Upload completed")

@login_required
# @transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            if request.user.is_teacher:
                profile_form = TeacherProfileForm(request.POST, instance=request.user.teacher)
            else:
                profile_form = StudentProfileForm(request.POST, instance=request.user.student)
            if profile_form.is_valid():
                profile_form.save()
                # messages.success(request, _('Your profile was successfully updated!'))
                return redirect('profile')
        elif request.POST.get("form_type") == 'formTwo':
            if request.user.is_teacher:
                profile_pic_form = TeacherProfilePicForm(request.POST, request.FILES, instance=request.user.teacher)
            else:
                profile_pic_form = TeacherProfilePicForm(request.POST, request.FILES, instance=request.user.student)

            if profile_pic_form.is_valid():
                profile_pic_form.save()
                return redirect('profile')

    else:
        if request.user.is_teacher:
            profile_form = TeacherProfileForm(instance=request.user.teacher)
            profile_pic_form = TeacherProfilePicForm(instance=request.user.teacher)
        else:
            profile_form = StudentProfileForm(instance=request.user.student)
            profile_pic_form = StudentProfilePicForm(instance=request.user.student)

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'profile_pic_form': profile_pic_form
    })

def markRealAttendence(request):
    # view = Attendance.objects.all().order_by('-date')
    form = AttendanceForm()
    date=datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request,"showAll.html",{'views':form,'users': Attendance.objects.filter(date=date).order_by('student__first_name'),'date':date})