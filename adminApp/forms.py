from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Person,Student

class AddPersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class AddStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
