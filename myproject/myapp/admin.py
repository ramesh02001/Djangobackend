from django.contrib import admin
from .models import User, Faculty, SubjectTab, Studenttab

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(SubjectTab)
admin.site.register(Studenttab)
