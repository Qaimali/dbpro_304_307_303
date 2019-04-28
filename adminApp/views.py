from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
# Create your views here.
from django.http import HttpResponse
from .models import Student, Person
from django.contrib.auth.models import User

import json
from .forms import AddStudentForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def Add_Student(request):

    form = AddStudentForm()
    return render(request, 'adminApp/addStudent.html', {'form': form})
