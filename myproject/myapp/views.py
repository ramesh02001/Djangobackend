

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Faculty, Studenttab, SubjectTab
from .serializers import UserSerializer, FacultySerializer, SubjectSerializer, StudentSerializer


# Register User
class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role
                }, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
#faculty CreateSubjectView
class CreateSubjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure that only faculty users can create a subject
        if request.user.role != 'faculty':
            return JsonResponse({"error": "Only faculty can create subjects."}, status=status.HTTP_403_FORBIDDEN)

        # Get the user who is creating the subject (faculty)
        user = request.user

        # Prepare the data for subject creation
        data = request.data
        data['user'] = user.id  # Automatically assign the logged-in user as the subject creator

        serializer = SubjectSerializer(data=data)

        if serializer.is_valid():
            serializer.save()  # Save the subject to the database
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# FacultyDashboard: Create Student
class CreateStudentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'faculty':
            return JsonResponse({"error": "Only faculty can create students."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#user listview
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class FacultyUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure only faculty users can access this endpoint
        if request.user.role != 'faculty':
            return JsonResponse(
                {"error": "Only faculty can view all students."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Retrieve all students (assuming role='student' identifies students)
        students = User.objects.filter(role='student')

        # Serialize the student records
        serializer = UserSerializer(students, many=True)

        # Return serialized student data
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

  
#facultyview all
class FacultyStudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure only faculty can access this endpoint
        if request.user.role != 'faculty':
            return JsonResponse({"error": "Only faculty can view all students."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve all student records
        students = Studenttab.objects.all()
        serializer = StudentSerializer(students, many=True)

        # Return serialized student data
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
#facultyupdatestudentprofile
class FacultyUpdateStudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, student_id):
        # Ensure that only faculty can update student details
        if request.user.role != 'faculty':
            return JsonResponse({"error": "Only faculty can update student details."}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the student by their ID
            student = Studenttab.objects.get(id=student_id)
        except Studenttab.DoesNotExist:
            return JsonResponse({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        # Update student details
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {"message": "Student details updated successfully.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 # StudentDashboard:  StudentProfileView
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the logged-in user

        # Ensure only students can access their profile
        if user.role != 'student':
            return JsonResponse({"error": "Access Denied. Only students can access their profile."}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the student profile associated with the logged-in user
            student_profile = Studenttab.objects.get(user=user)
            student_data = StudentSerializer(student_profile).data

            # Add user-specific fields (email and username) to the response
            student_data['email'] = user.email
            student_data['username'] = user.username

            # Fetch and include subject names
            subjects = student_profile.subjects.all()
            student_data['subjects'] = [{"id": subject.id, "name": subject.name} for subject in subjects]

            return JsonResponse(student_data, status=status.HTTP_200_OK)

        except Studenttab.DoesNotExist:
            return JsonResponse({"error": "Your student profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

#UpdateStudentProfileView
class UpdateStudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user  # Get the logged-in user

        # Ensure only students can update their profile
        if user.role != 'student':
            return JsonResponse({"error": "Access Denied. Only students can update their profile."}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Fetch the student profile associated with the logged-in user
            profile = Studenttab.objects.get(user=user)

            # Use the serializer to validate and update the profile data
            serializer = StudentSerializer(profile, data=request.data, partial=True)
            
            # If subjects are included in the request, update them
            if 'subjects' in request.data:
                # Get the subject IDs from the request data
                subject_ids = request.data.get('subjects')
                try:
                    # Fetch the subject objects by their IDs
                    subjects = SubjectTab.objects.filter(id__in=subject_ids)
                    
                    # Update the student's subjects
                    profile.subjects.set(subjects)  # Using set() to overwrite the current subjects
                except SubjectTab.DoesNotExist:
                    return JsonResponse({"error": "One or more subjects not found."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate and save the profile
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)

            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Studenttab.DoesNotExist:
            return JsonResponse({"error": "Your student profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
# Fetch all subjects from the database

class SubjectListView(APIView):
    """
    API endpoint to retrieve all available subjects.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the logged-in user

        # Ensure only students and faculty can access subjects
        if user.role not in ['student', 'faculty']:
            return JsonResponse(
                {"error": "Access Denied. Only students and faculty can access subjects."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            # Fetch all subjects from the database
            subjects = SubjectTab.objects.all()

            # Serialize the subjects
            serializer = SubjectSerializer(subjects, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Return a detailed error message
            return JsonResponse(
                {"error": f"Failed to retrieve subjects: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
