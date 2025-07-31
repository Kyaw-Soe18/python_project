from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Course(models.Model):
    courseshortname = models.CharField(max_length=250,default='True')
    coursefullname = models.CharField(max_length=250,default='True')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.coursefullname + (self.courseshortname)

class Subjects(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject1 = models.CharField(max_length=250,default='True')
    subject2 = models.CharField(max_length=250,default='True')
    subject3 = models.CharField(max_length=250,default='True')
    subject4 = models.CharField(max_length=250,default='True')
    subject5 = models.CharField(max_length=250,default='True')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Student(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    subjects_id = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=50, unique=True)
    session = models.CharField(max_length=250,default='True')
    fname = models.CharField(max_length=250,default='True')

    gender = models.CharField(max_length=250,default='True')


    nation = models.CharField(max_length=250,default='True')
    mobno = models.CharField(max_length=250,default='True')
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.fname

from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subjects', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} on {self.date} - {self.status}"
