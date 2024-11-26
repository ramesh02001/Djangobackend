# from rest_framework import serializers
# from .models import *

# class Product_Serializers(serializers.ModelSerializer):
#     class Meta:
#         model=Products
#         fields = '__all__'

# class Product_Serializers2(serializers.ModelSerializer):
#     class Meta:
#         model=Products
#         fields = ['Product_name']  


# class categeoryserializer(serializers.ModelSerializer):
#     class Meta:
#         model=Category
#         fields='__all__'       


# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from .models import *


# #User serializer

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= User
#         fields=['id','username','email','role','password']
#         extra_Kwargs={'password':{'write_only': True}}

#     def create(self, validated_data):
#         validated_data['password']= make_password(validated_data['password'])#encrympt
#         return super(UserSerializer,self).create(validated_data)   
    

# #subject serializer
# class SubjectSerializer(serializers.ModelSerializer):
#     faculty=UserSerializer(read_only=True)

#     class Meta:
#        model=Subject
#        fields = ['id', 'name', 'faculty']


# #student profile serializer

# class StudentProfileSerializer(serializers.ModelSerializer):
#     user=UserSerializer()
#     subject=SubjectSerializer(many=True)

#     class Meta:
#         model=Student
#         fields='__all__'


# # Student Profile Create Serializer
# class StudentProfileCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = '__all__'
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Faculty, SubjectTab, Studenttab


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)


# Faculty Serializer
class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


# Subject Serializer
class SubjectSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = SubjectTab
        fields = '__all__'


# Student Serializer
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studenttab
        fields = '__all__'
