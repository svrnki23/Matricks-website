from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse #is used to generate the URL of a view based on its name (defined in the urls.py file). 
                                #It allows you to dynamically create URLs instead of hardcoding them
from django.core.files.storage import FileSystemStorage #allows to save, retrieve, and deletes files
from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, FeedBackStudent
import datetime


def studentHome(request):
    student_obj = Students.objects.get(admin=request.user.id) #queries the Students model to find the record where admin matches the logged-in user's ID.
    totalAttendance = AttendanceReport.objects.filter(student_id = student_obj).count() #retrieves all the attendance records for a student
    days_present = AttendanceReport.objects.filter(student_id = student_obj, status = True).count() #retrieves the days a student was present
    days_absent = AttendanceReport.objects.filter(student_id = student_obj, status = False).count() #retrieves the days a student was absent
    
    course_obj = Courses.objects.get(id = student_obj.course_id.id)
    total_courses = Subjects.objects.filter(course_id=course_obj).count()
    
    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(course_id = student_obj.course_id) #student_obj.course_id referneces the courses the student is enrolled in
                                                                              #the objects.filter queries the subjects model to get all the subjects
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id = subject.id) #retrieves all attendance records for this current subject
        #filters attendancereport to include only records in this current subject's attendance list, ensures its specific to the current student
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in = attendance, status = True, student_id = student_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in = attendance, status = False, student_id = student_obj.id).count()
        
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
        
        #creating a context dictionary to pass data to the template for rendering.
        #template will have access to all the attendance stats to display to the student
        context = {
            "total_attendance": totalAttendance,
            "attendance_present": days_present,
            "attendance_absent":days_absent,
            "total_subjects":total_courses,
            "subject_name":subject_name,
            "data_present": data_present,
            "data_absent":data_absent,
        }
        
        return render(request,"student_template/student_home_template.html")
    
def student_view_attendance(request):
    
    #getting logged into student data
    student = Students.objects.get(admin=request.user.id)
    
    #getting courses enrolled for logged in student
    course = student.course_id
    
    #getting the subjects of the course enrolled
    subjects = Subjects.objects.filter(course_id = course)
    
    context = {
        "subjects":subjects,
    }

    return render(request,"student_template/student_view_attendance.html",context)

def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        #getting all the input data from the student
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        #parsing the data into python object
        start_date_parse = datetime.datetime.strptime(start_date,'%m-%d-%Y').date()
        end_date_parse = datetime.datetime.strptime(end_date,'%m-%d-%Y').date()
        
        #getting all the subject data based on seleected subject
        subject_obj = Subjects.objects.get(id=subject_id)
        #getting logged into user data
        user_obj = CustomUser.objects.get(id=request.user.id)
        #getting student data based on logged in data
        stud_obj = Students.object.get(admin=user_obj)
        
        attendance = Attendance.objects.filter(attendance_data_range= (start_date_parse,end_date_parse), subject_id = subject_obj)
        
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in = attendance, student_id = stud_obj)
        
        context = {
            "subject_obj": subject_obj,
            "attendance_reports":attendance_reports
        }
        
        return render(request,'student_template/student_attendance_data.html',context)

def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    
    context = {
        "user":user,
        "student":student,
    }
    
    return render(request,'sutdent_template/student_profile.html',context)

def student_profile_view(request):
    if request.method != "POST":
        messages.error(request,"Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')
        
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            
            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request,"Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request,"Failed to Update Profile")
            return redirect('student_profile')
        
# def student_view_result(request):
#     student=Students.objects.get(admin=request.user.id)
#     student_result = StudentResult.objects.filter(student_id = student.id)
    
#     context = {
#         "student_result":student_result,
#     }
    
#     return render(request,"student_template/student_view_result.html",context)

    

    
        
    
    

    