import datetime
from django.forms.widgets import HiddenInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Person, Student, SubjectClass, Calender

from datetimepicker.widgets import DateTimePicker


class AddPersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            self.base_fields['FirstName'].initial = instance.FirstName
            self.base_fields['LastName'].initial = instance.LastName
            self.base_fields['FatherName'].initial = instance.FatherName
            self.base_fields['Cnic'].initial = instance.Cnic
            self.base_fields['Address'].initial = instance.Address
            self.base_fields['Contact'].initial = instance.Contact
        forms.ModelForm.__init__(self, *args, **kwargs)
    FirstName = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'vTextField', 'required': True}))
    LastName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField'}))
    FatherName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField'}))
    Cnic = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'vTextField'}))
    Address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField'}))
    Contact = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'vTextField'}))

    class Meta:
        model = Person
        fields = '__all__'


class AddStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


YEAR_CHOICES = ((1, 'Ist'), (2, '2nd'), (3, '3rd'), (4, '4th'),
                (5, '5th'), (6, '6th'), (7, '7th'), (8, '8th'))


class DateInput(forms.DateInput):
    input_type = 'date'


class DateForm(forms.ModelForm):

    class Meta:
        model = Calender
        fields = ['date_Time']
        widgets = {
            'date_Time': DateInput(),
        }


class AddClassSubjectForm(ModelForm):
    SemsterName = forms.ChoiceField(
        choices=YEAR_CHOICES, widget=forms.Select, label='Select Semster')

    class Meta:
        model = SubjectClass
        fields = '__all__'
