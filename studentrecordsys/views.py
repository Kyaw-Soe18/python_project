from django.shortcuts import render,redirect,HttpResponse
from srsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from srsapp.models import CustomUser,Course,Subjects,Student
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import logging
import random
from django.shortcuts import get_object_or_404
from datetime import datetime
User = get_user_model()

def BASE(request):
       return render(request,'base.html')

@login_required(login_url='/')
def DASHBOARD(request):
    course_count = Course.objects.all().count
    sub_count = Subjects.objects.all().count
    student_count = Student.objects.all().count
    context = {
        'course_count':course_count,
        'sub_count':sub_count,
        'student_count':student_count,
    }
    return render(request,'dashboard.html',context)

def LOGIN(request):
    return render(request,'login.html')

def doLogin(request):
    if request.method == 'POST':
        user = EmailBackEnd.authenticate(request,
                                         username=request.POST.get('email'),
                                         password=request.POST.get('password')
                                         )
        if user!=None:
            login(request,user)
            return redirect('dashboard')
            
        else:
                messages.error(request,'Email or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Email or Password is not valid')
            return redirect('login')
        


def doLogout(request):
    logout(request)
    return redirect('login')

login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)

@login_required(login_url = '/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            if password !=None and password != "":
                customuser.set_password(password)
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'profile.html')
@login_required(login_url = '/')
def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')

@login_required(login_url = '/')
def ADD_COURSES(request):
    if request.method == "POST":
        coursesn = request.POST.get('courseshortname')
        coursefn = request.POST.get('coursefullname')
        courses = Course(courseshortname=coursesn, coursefullname = coursefn
        )
        courses.save()
        messages.success(request, 'Course Added Succeesfully!!!')
        return redirect("add_courses")
    return render(request,'add-courses.html')

def MANAGE_COURSES(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'manage_course.html', context)

def DELETE_COURSES(request,id):
    courses = Course.objects.get(id=id)
    courses.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_courses')

login_required(login_url='/')
def UPDATE_COURSES(request,id):
    courses = Course.objects.get(id=id)
    
    context = {
         'courses':courses,
    }

    return render(request,'update_course.html',context)

def UPDATE_COURSES_DETAILS(request):
        if request.method == 'POST':
          c_id = request.POST.get('course_id')
          courseshortname = request.POST.get('courseshortname')
          coursefullname = request.POST.get('coursefullname')
          course= Course.objects.get(id=c_id) 
          course.courseshortname = courseshortname
          course.coursefullname = coursefullname
          course.save()   
          messages.success(request,"Your course detail has been updated successfully")
          return redirect('manage_courses')
        return render(request, 'update_course.html')

@login_required(login_url = '/')
def ADD_SUBJECT(request):
    course = Course.objects.all()
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        subject1 = request.POST.get('subject1')
        subject2 = request.POST.get('subject2')
        subject3 = request.POST.get('subject3')
        subject4 = request.POST.get('subject4')
        subject5 = request.POST.get('subject5')
        cid =Course.objects.get(id=course_id)
        subjects = Subjects(course_id=cid, subject1 = subject1,subject2=subject2,
        subject3 = subject3, subject4 = subject4, subject5 = subject5
        )
        subjects.save()
        messages.success(request, 'Subject Added Succeesfully!!!')
        return redirect("add_subject")
    context = {
        'course':course
    }
    return render(request,'add-subject.html',context)


def MANAGE_SUBJECT(request):
    subjects = Subjects.objects.all()
    context = {
        'subjects': subjects,
    }
    return render(request, 'manage_subject.html', context)

def DELETE_SUBJECT(request,id):
    subjects = Subjects.objects.get(id=id)
    subjects.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_subject')


def REGISTER_STUDENTS(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        courses = Course.objects.all()
        context = {'courses': courses,}
        return render(request, 'reg-students.html', context)
    else:
        # If it's not a POST request, you might want to handle that case accordingly
        # For example, render the form without subjects selected
        courses = Course.objects.all()
        context = {'courses': courses}
        return render(request, 'reg-students.html', context)
        
def REGISTER_STUDENTS(request):
    course = Course.objects.all()
    if request.method == "POST":

        if request.method == "POST":
            course_id = request.POST.get('course_id')
            roll_number = request.POST.get('roll_number')

            if not course_id:
                messages.error(request, "Please select a course.")
                context = {'course': course}
                return render(request, 'reg-students.html', context)

            try:
                course_instance = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                messages.error(request, "Selected course does not exist.")
                context = {'course': course}
                return render(request, 'reg-students.html', context)
        try:
            subject_instance = Subjects.objects.get(course_id=course_instance)
        except Subjects.DoesNotExist:
            messages.error(request, "No subjects found for selected course.")
            context = {'course': course}
            return render(request, 'reg-students.html', context)


        roll_number = request.POST.get('roll_number')
        session = request.POST.get('session')
        fname = request.POST.get('fname')
        gender = request.POST.get('gender')

        mobno = request.POST.get('mobno')
        email = request.POST.get('email')

        # Check if roll number already exists (optional)
        if Student.objects.filter(roll_number=roll_number).exists():
            messages.error(request, "Roll number already exists. Please enter a unique roll number.")
            context = {'course': course}
            return render(request, 'reg-students.html', context)
        course_instance = Course.objects.get(id=course_id)

        stu = Student(course_id=course_instance ,subjects_id=subject_instance,
                      roll_number=roll_number,session=session,
                       fname = fname,gender=gender, mobno=mobno,email=email,
        )
        stu.save()
        messages.success(request, 'Student registered Succeesfully!!!')
        return redirect("reg_students")
    context = {
        'course':course
    }
    return render(request, 'reg-students.html', context)


def get_subjects(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        sub = Subjects.objects.filter(course_id=c_id)
        subject_options = ''
        for subject in sub:
            subject_options += f'<option value="{subject.id}">{subject.subject1}+{subject.subject2}+{subject.subject3}+{subject.subject4}+{subject.subject5}</option>'
        return JsonResponse({'subject_options': subject_options})
    
def MANAGE_STUDENTS(request):
    stu = Student.objects.all()
    context = {
        'stu': stu,
    }
    return render(request, 'manage_students.html', context)

def delete_Students(request, id):
    try:
        stu = get_object_or_404(Student, id=id)
        stu.delete()
        messages.success(request, 'Record Deleted Successfully!!!')
    except Student.DoesNotExist:
        messages.error(request, 'Student does not exist.')
    return redirect('manage_students')

def UPDATE_STUDENTS(request,id):
    course = Course.objects.all()
    student = Student.objects.get(id=id)
    
    context = {
         'student':student,
         'course':course,
    }

    return render(request,'update_student.html',context)

def UPDATE_STUDENTS_DETAILS(request):
        if request.method == 'POST':
          s_id = request.POST.get('student_id')
          session = request.POST.get('session')
          fname = request.POST.get('fname')
          roll_number = request.POST.get('roll_number')
          gender = request.POST.get('gender')
          ph = request.POST.get('ph')
          mobno = request.POST.get('mobno')
          email = request.POST.get('email')
          course_id = request.POST.get('course_id')  # This was missing
          #stu= Student.objects.get(id=s_id)
          student = get_object_or_404(Student, id=s_id)
          student.session = session
          student.fname = fname
          student.roll_number = roll_number
          student.gender = gender
          student.ph = ph
          student.mobno = mobno
          student.email = email
          try:
              course = Course.objects.get(id=course_id)
              student.course_id = course

              # Automatically assign the correct subject set
              subject = Subjects.objects.get(course_id=course)
              student.subjects_id = subject
          except Course.DoesNotExist:
              messages.error(request, "Selected course not found.")
          except Subjects.DoesNotExist:
              student.subjects_id = None  # If no subjects exist, set null
          student.save()
          messages.success(request,"Your student detail has been updated successfully")
          return redirect('manage_students')
        return render(request, 'update_student.html')



def data_between_dates(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    stu = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'data_between_dates.html', {'stu': stu, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        stu = Student.objects.filter(created_at__range=(start_date, end_date))

    return render(request, 'data_between_dates.html', {'stu': stu,'start_date':start_date,'end_date':end_date})
    



def Search_Students(request):    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where Roll Number or Mobile Number contains the query
            stu = Student.objects.filter(roll_number__icontains=query) | Student.objects.filter(mobno__icontains=query)
            #messages.success(request, "Search against " + query)
            return render(request, 'search-students.html', {'stu': stu, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'search-students.html', {})


