from django.shortcuts import render
from srsapp.models import Student, Subjects

def attendance_report(request):
    student = None
    subjects = []
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    if request.method == "GET":
        ykpt = request.GET.get('ykpt')
        if ykpt:
            try:
                student = Student.objects.get(roll_number=ykpt)
                subject_obj = student.subjects_id
                if subject_obj:
                    subjects = [
                        subject_obj.subject1,
                        subject_obj.subject2,
                        subject_obj.subject3,
                        subject_obj.subject4,
                        subject_obj.subject5,
                    ]
            except Student.DoesNotExist:
                student = None

    context = {
        'student': student,
        'subjects': subjects,
        'weeks': weeks,
        'days': days,
    }
    return render(request, 'attendance_report.html', context)

