from django.urls import path
from . import views

urlpatterns = [
    path('attendance-report/', views.attendance_report, name='attendance_report'),
]

