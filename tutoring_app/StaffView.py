from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core import serializers
import json

from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, FeedBackStudent, SessionYearModel

def staff_home(request):
    
    #fetching all student data under the staff member
    print(request.user.id)
    subjects = Subjects.objects.filter(staff_id = request.user.id) #fetches all the subjects that are assigned to this staff member(tutor)
    print(subjects)
    
    course_id_list = [] #to create a list of course ids associated with the subject
    for subject in subjects:
        course = Courses.objects.filter(id = subject.course_id.id) #for each subject, fetches the courses to which the subject belongs
        course_id_list.append(course.id)
        
    final_course = []
    
    for course_id in course_id_list:
        #removing duplicate course ids
        if course_id not in course_id_list:
            final_course.append(course_id)
    print(final_course)
    
    students_count = Students.objects.filter(course_id__in = final_course).count() #counts the num of students enrolled in the course taught by the staff
    subject_count = subjects.count()
    
    #Fetch all attendance records for all subjects taught by that staff
    attendance_count = Attendance.objects.filter(subject_id__in = subjects).count() 
    
    #fetch attendance data by subjects
    subject_list = []
    attendance_list = []
    
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id = subject.id).count() #counting attendance for that specific subject
        subject_list.append(subject.subject_name) #adding the name of that subject
        attendance_list.append(attendance_count1) #adding the attendance count in a parallel list
    
    students_attendance = Students.objects.filter(course_id__in = final_course) 
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    #fetching the attendance data for each specific student and adding to a list for display
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id = student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id = student.id).count()
        
        student_list.append(student.admin.first_name + " " + student.admin.last_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
        
    context = {
        "students_count":students_count,
        "attendance_count":attendance_count,
        "subject_count":subject_count,
        "subject_list":subject_list,
        "attendance_list":attendance_list,
        "student_list":student_list,
        "attendance_present_list":student_list_attendance_present,
        "attendance_absent_list":student_list_attendance_absent,
    }
    
    return render(request, "staff_template/staff_home_template.html",context)

#provides a page where staff members(tutors) can take attendance for their classes
def staff_take_attendance(request): #fetch the subjects that the staff is assigned to 
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    session_years = SessionYearModel.objects.all() #provide a list of session years
    context = {
        "subjects":subjects,
        "session_years":session_years,
    } #
    
    return render(request,"staff_template/take_attendance_template.html",context)

#disables the CSRF protection for this view, meaning this view will accept requests without requiring a CSRF token.
#This is typically used when the request is coming from external systems or APIs where including a CSRF token isn't feasible 
@csrf_exempt
def get_students(request):
    subject_id = request.POST.get('subject')
    session_year = request.POST.get('session_year')
    
    #students enroll to course, course has specific subjects
    #getting all data from subject model based on the subject_id
    
    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year)
    
    students = Students.objects.filter(course_id = subject_model.course_id, session_year_id = session_model)
    
    #only passing student id and name 
    list_data = []
    
    for student in students:
        data_small = {"id":student.admin.id, "name":student.admin.first_name + " " + student.admin.last_name}
    list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data), content_type = "application/json", safe=False)    



#def save_attendance_data(request):


#def staff_update_attendance(request):


#@csrf_exempt
#def get_attendance_dates(request):

#@csrf_exempt
#def get_attendance_student(request):

#@csrf_exempt
#def update_attendance_data(request):

#def staff_profile(request):

#def staff_profile_update(request):


    
    
    
    
        



