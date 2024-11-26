
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now

# Custom User Model

class User(AbstractUser):
    ROLE_CHOICES = (
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(default=now)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Avoid conflict with 'auth.User.groups'
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Avoid conflict with 'auth.User.user_permissions'
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

# Faculty Model
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'faculty'})
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Faculty: {self.user.username}"


# Subject Model
class SubjectTab(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.name

# Student Model
class Studenttab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    first_name = models.CharField(max_length=50, blank=True, null=True)  # New field
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices= [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
])
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    subjects = models.ManyToManyField(SubjectTab, related_name='enrolled_students')

    def __str__(self):
        return f"Student: {self.user.username}"
