from django.db import models
from django.contrib.auth.models import AbstractUser #creates a custom user model, abstract user includes default user fields like username, email, password
from django.db.models.signals import post_save #used when you want to create related models when a CustomUser is created, or sending notifs after saving a user
from django.dispatch import receiver #links the signal post_save to a specific function, ex: creating related models
from django.core.mail import send_mail #django utility function used to send emails
from django.conf import settings
from django.template.loader import render_to_string #renders a template to string
# Create your models here.

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True) #automatically generates an integer that uniquely identifies each record
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager() #not required since django automattically creates one
    
    def __str__(self):
        return f"Session from {self.session_start_year} to {self.session_end_year}"

class CustomUser(AbstractUser):
    STAFF = '1'
    STUDENT = '2'

    user_type_data = (
        (STAFF, "Staff"),
        (STUDENT, "Student"),
    )
    user_type = models.CharField(
        choices=user_type_data,
        max_length=10,
        default=STUDENT
    )
    
    user_type_date = ((STAFF,"staff"), (STUDENT,'student'))
    user_type = models.CharField(default=2, choices=user_type_data, max_length=10)
    
class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE) #each record in this model is linked to ONE record in customuser, no duplicates. deletes the current model if customuser is deleted
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) #automatically adds the field to current date and time when record is created
    updated_at = models.DateTimeField(auto_now=True) #automatically sets the field to current date and time when record is updated
    objects = models.Manager()
    
class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True) #tracks when a subject was added or last updated
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_picture = models.FileField()
    username = models.TextField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default = 1)
    session_year_id = models.ForeignKey(SessionYearModel, null=True, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) #tracks when a student registered or changed profile 
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) #tracks when attendance was logged 
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) #tracks when logging attendance status changes for a student
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#signal that listens for the post_save event on the CustomUser model. 
@receiver(post_save, sender=CustomUser)

def creater_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 2:
            Students.objects.create(admin=instance, course_id = Courses.objects.get(id=1), 
                                    session_year_id = SessionYearModel.objects.get(id=1), address="", profile_pic = "", gender="")
    
@receiver(post_save, sender=CustomUser)

def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.staffs.save()
    if instance.user_type == 2:
        instance.students.save()
 

@receiver(post_save, sender=CustomUser)          
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Matricks Tutoring"
        message = render_to_string('emails/confirmation_email.html', {'user':instance})
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False, #exception will be raised if an error occurs while sending an email
        )
        
# <!-- templates/emails/confirmation_email.html -->
# <html>
# <body>
#     <h1>Welcome, {{ user.first_name }}!</h1>
#     <p>Thank you for registering with us. We're excited to have you on board!</p>
#     <p>If you didn't register for this account, please ignore this email.</p>
#     <p>Best regards,<br>The Tutoring Platform Team</p>
# </body>
# </html>