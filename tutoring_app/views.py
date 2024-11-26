from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect 
#redirect function redirects user to a different url or view
#HttpResponeRedirect creates a HTTP 302 request response, required you to provide entire url to be redircted to which is unlike the redirect function
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages #provides user with notifications
from .models import CustomUser, Staffs, Students

# Create your views here.
def home(request):
    return render(request,'home.html') # request passed as the first argument to render.
                                       #it ensures that the template is rendered in the context of the current HTTP request.
                                       
def contact(request):
    return render(request, 'contact.html')

def loginUser(request):
    return render(request, 'login_page.html')

def dologin(request):
    print("here")
    
    email_id = request.GET.get('email') # retrieve the value of a query parameter from the URL in a safe and convenient way.
    password = request.GET.get('password')
    
    print(email_id)
    print(password)
    print(request.user)
    
    if not (email_id and password):
        messages.error(request, "Please provide both email and password")
        return render(request, 'login_page.html')
    
    #If a user with the specified email and password exists, the last matching user is retrieved and assigned to user.
    user = CustomUser.objects.filter(email=email_id, password=password).last()
    
    if not user:
        messages.error(request, "Invalid login credentials")
        return render(request, 'login_page.html')
    
    login(request,user)
    print(request.user)
    
    if user.user_type == CustomUser.STUDENT:
        return redirect('student_home/')
    if user.user_type == CustomUser.STAFF:
        return redirect('staff_home/')
    
    return render(request,'home.html')
    

def register(request):
    return render(request,'register.html')

def doRegister(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')
    user_type = request.GET.get('user_type')
    
    print(first_name)
    print(last_name)
    print(email_id)
    print(password)
    print(confirm_password)
    
    if not (email_id and password and confirm_password):
        messages.error(request, "Please provide all the details")
        return render(request, 'regsiter.html')
    
    if password != confirm_password:
        messages.error(request,"Passwords do not match, Try Again!")
        return render(request,'register.html')
    
    is_user_exists = CustomUser.objects.filter(email=email_id).exists() #check if the given email is already in the database or not
    
    if is_user_exists:
        messages.error(request,"User with this email already exists")
        return render(request, 'register.html')
    
    user = CustomUser() #creates a custom user based on the given user after the info was properly authenticated
    user.email = email_id
    user.password = password
    user.user_type = user_type.lower()
    user.first_name = first_name
    user.last_name = last_name
    user.save()
    
    if user_type.lower() == 'staff': #assigns whether the user is a staff member or student based on their given input
        Staffs.object.create(admin=user)
    elif user_type.lower() == 'student':
        Students.object.create(admin=user)
    else:
        messages.error(request,"Invalid User Type. Please select student or staff.")
        return render(request, 'register.html')
    
    messages.success("Registration Successful! Please log in")
    return render(request,'login_page.html') 

def logout(request):
    logout(request)
    return HttpResponseRedirect('/')