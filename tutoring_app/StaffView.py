from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.core import serializers
import json

from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, FeedBackStudent, SessionYearModel

def staff_home(request):
    
    #fetching all student data under the staff member
    print(request.user.id)
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    print(subjects)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.filter(id = subject.course_id.id)
        course_id_list.append(course.id)
        
    final_course = []
    
    for course_id in course_id_list:
        #removing duplicate course ids
        if course_id not in course_id_list:
            final_course.append(course_id)
    print(final_course)
    
    students_count = Students.objects.filter(course_id__in = final_course).count()
    subject_count = subjects.count()
    
    #Fetch all attendance count
    attendance_count = Attendance.objects.filter(subject_id__in = subjects).count()
    
    
        



