# from django.urls import path
# from .views import *

# urlpatterns=[
#     path('product/',ProductView.as_view()),
#     path('product/<int:id>/',productviewbyid.as_view()),
#     path('category/',CategoryView.as_view())
# ]
from django.urls import path
from .views import RegisterUserView,FacultyUpdateStudentProfileView, LoginView, CreateStudentView,FacultyUserListView, FacultyStudentListView, StudentProfileView,CreateSubjectView,SubjectListView, UpdateStudentProfileView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('subjects/', CreateSubjectView.as_view(), name='create_subject'),
    path('faculty/create-student/', CreateStudentView.as_view(), name='create_student'),
    path('faculty/user/', FacultyUserListView.as_view(), name='faculty user'),
    path('faculty/students/', FacultyStudentListView.as_view(), name='faculty_students'),
    path('student/profile/', StudentProfileView.as_view(), name='student_profile'),
    path('student/update-profile/', UpdateStudentProfileView.as_view(), name='update_profile'),
    path('student/subjects/', SubjectListView.as_view(), name='subject-list'),
    path('faculty/update-student/<int:student_id>/', FacultyUpdateStudentProfileView.as_view(), name='update_subject'),
]
