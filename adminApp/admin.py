from django.db.models import Count, DateTimeField, DateField
from .forms import *
from django.db.models.functions import Trunc
from django.template.response import TemplateResponse
from django.contrib import admin
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve, path
from django.utils.html import format_html
from .models import *
from .render import Render
# Register your models here.
from django.forms.models import BaseInlineFormSet
admin.site.site_header = 'Learning Managemnet System'
admin.site.site_title = 'LMS'

admin.site.index_title = 'Admin'


class myAttendanceAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class ClassInline(admin.TabularInline):
    model = Class
    list_display_links = ('Name')
    extra = 0


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 0


class SectionInline(admin.TabularInline):

    model = Section
    extra = 0


class ExamInline(admin.StackedInline):

    model = Exam
    extra = 0

    def Paper(self, instance):
        url = reverse('admin:adminApp_exam_change', args=(instance.id,))
        return format_html(u'<a href="{}">{}</a>', url, instance.Name)
    readonly_fields = ('Paper',)
    fieldsets = [
        (None,               {'fields': ['Paper']}),
        ('Exam information', {'fields': [
         'Name', 'ClassId', 'SectionId', 'SubjectId', 'startTime'], 'classes': ['collapse']}),
    ]


class EmployessInline(admin.TabularInline):

    model = Employee
    extra = 0

    def Employee(self, instance):
        url = reverse('admin:adminApp_employee_change', args=(instance.id,))
        return format_html(u'<a href="{}">{}</a>', url, instance.PersonId)
    readonly_fields = ('Employee',)

    fieldsets = [
        (None,               {'fields': ['Employee']}),
        ('Job information', {'fields': [
         'Designation', 'Salary'], 'classes': ['collapse']}),
    ]


class ProgramInline(admin.StackedInline):
    model = Program
    extra = 0

    def Program(self, instance):
        url = reverse('admin:adminApp_program_change', args=(instance.id,))
        return format_html(u'<a href="{}">{}</a>', url, instance.Name)
    readonly_fields = ('Program',)

    fieldsets = [
        (None,               {'fields': ['Program']}),
        ('Program information', {'fields': [
         'Name', 'EntryTest', 'MeritList', 'FeeSubmission', 'ClassesCommence'], 'classes': ['collapse']}),
    ]


class DepartmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['Name', 'InstitueId', 'Contact']},),

    ]
    search_fields = ('Name',)
    inlines = [ProgramInline, SubjectInline, EmployessInline, ExamInline]
    list_filter = ('Name',)


class myProgramAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    change_form_template = 'adminApp/changeProgram.html'

    # inlines = [ClassInline]

    fieldsets = [
        (None,               {'fields': ['Name', 'DepartmentId']}),
        ('Admission information', {'fields': [
         'EntryTest', 'MeritList', 'FeeSubmission', 'ClassesCommence'], 'classes': ['collapse']}),
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        depId = Program.objects.get(pk=object_id).DepartmentId
        extra_context['osm_data'] = Class.objects.filter(
            ProgramId=object_id, DepartmentId=depId)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class mySectionAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    change_form_template = 'adminApp/changeSection.html'
    sectionSemster_template = 'adminApp/sectionSemster.html'
    sectionSubjects_template = 'adminApp/sectionSubjects.html'
    markAttendance_template = 'adminApp/markAttendance.html'
    markEvaluation_template = 'adminApp/markEvaluation.html'
    updateEvaluation_template = 'adminApp/updateEvaluation.html'
    subjectAttendance_template = 'adminApp/subjectAttendance.html'
    attendanceDetails_template = 'adminApp/attendanceDetails.html'
    attendanceDetailsReport_template = 'adminApp/attendanceDetailReport.html'
    def get_urls(self):

        urls = super().get_urls()
        my_urls = [
            path('<int:SecId>/Semster', self.admin_site.admin_view(
                self.sectionSemster_view), name='adminApp_section_semster_list'),
            path('<int:SecId>/Student/pdf', self.admin_site.admin_view(
                self.StudentList_Report), name='adminApp_section_student_pdf'),
            path('Evaluation/<int:examId>', self.admin_site.admin_view(
                self.markEvaluation_view), name='adminApp_section_evaluation'),
            path('Evaluation/<int:examId>/pdf', self.admin_site.admin_view(
                self.Evaluation_Report), name='adminApp_section_evaluation_pdf'),
            path('<int:SecId>/semster/<int:SemsterId>', self.admin_site.admin_view(
                self.sectionSubjects_view), name='adminApp_section_subjects'),
            path('<int:SecId>/semster/<int:SemsterId>/attendance/<int:subjectId>', self.admin_site.admin_view(
                self.markAttendance_view), name='adminApp_section_attendance'),
            path('<int:SecId>/semster/<int:SemsterId>/attendance/<int:subjectId>/list', self.admin_site.admin_view(
                self.subjectAttendance_view), name='adminApp_subject_attendance'),
            path('<int:SecId>/semster/<int:SemsterId>/attendance/<int:subjectId>/pdf', self.admin_site.admin_view(
                self.subjectAttendance_pdf), name='adminApp_subject_attendance_pdf'),
            path('<int:SecId>/semster/<int:attendanceId>/attendance/<int:subjectId>/details', self.admin_site.admin_view(
                self.attendanceDetail_view), name='adminApp_attendance_detail'),
            path('<int:SecId>/Subject/<int:attendanceId>/attendance/<int:subjectId>/pdf', self.admin_site.admin_view(
                self.getPdf_view), name='adminApp_attendance_pdf')
        ]
        return my_urls + urls

    add_form_template = 'adminApp/addSection.html'
    def add_view(self, request, form_url='', extra_context=None):

        return super(mySectionAdmin, self).add_view(request, form_url)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        depId = Section.objects.get(pk=object_id).DepartmentId
        proId = Section.objects.get(pk=object_id).ProgramId
        class_Id = Section.objects.get(pk=object_id).ClassId
        extra_context['osm_data'] = Student.objects.filter(
            SectionId=object_id, DepartmentId=depId, ProgramId=proId, ClassId=class_Id)
        extra_context['evaluations'] = Exam.objects.filter(
            SectionId=object_id, DepartmentId=depId, ClassId=class_Id)
        extra_context['section_id'] = object_id
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def sectionSemster_view(self, request, SecId):
        student_list = Student.objects.filter(SectionId=SecId)
        return render(request, self.sectionSemster_template, {'n': range(8), 'SectionId': SecId})

    def getPdf_view(self, request, SecId, attendanceId, subjectId):
        attendanceDate = Attendance.objects.get(id=attendanceId).Date
        subjectName = Subject.objects.get(id=subjectId)
        sectionName = Section.objects.get(id=SecId)
        semsterNumber = SubjectClass.objects.get(
            SubjectId=subjectId).SemsterName
        classId = Section.objects.get(id=SecId).ClassId
        details = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId)
        totalPresent = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId, status=1).count()
        totalAbsent = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId, status=0).count()
        try:
            SemsterName = SubjectClass.objects.get(
                SubjectId=subjectId).SemsterName
        except Exception as e:
            SemsterName = SubjectClass.objects.filter(
                SubjectId=subjectId)[0].SemsterName

        return Render.render('adminApp/attendanceDetailReport.html',  {'details': details, 'totalPresent': totalPresent, 'totalAbsent': totalAbsent, 'attendanceId': attendanceId, 'attendancedate': attendanceDate, 'SemsterName': semsterNumber, 'subjectId': subjectName, 'classId': classId, 'SectionId': sectionName})

    def attendanceDetail_view(self, request, SecId, attendanceId, subjectId):
        attendanceDate = Attendance.objects.get(id=attendanceId).Date
        subjectName = Subject.objects.get(id=subjectId)
        sectionName = Section.objects.get(id=SecId)
        semsterNumber = SubjectClass.objects.get(
            SubjectId=subjectId).SemsterName
        classId = Section.objects.get(id=SecId).ClassId
        details = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId)
        totalPresent = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId, status=1).count()
        totalAbsent = Attendance.objects.filter(
            Date=attendanceDate, SubjectId=subjectId, status=0).count()
        try:
            SemsterName = SubjectClass.objects.get(
                SubjectId=subjectId).SemsterName
        except Exception as e:
            SemsterName = SubjectClass.objects.filter(
                SubjectId=subjectId)[0].SemsterName

        return render(request, self.attendanceDetails_template, {'details': details, 'totalPresent': totalPresent, 'totalAbsent': totalAbsent, 'attendanceId': attendanceId, 'attendancedate': attendanceDate, 'SemsterName': semsterNumber, 'subjectId': subjectName, 'classId': classId, 'SectionId': sectionName})

    def subjectAttendance_pdf(self, request, SecId, SemsterId, subjectId):
        dates = Attendance.objects.annotate(Date_group=Trunc(
            'Date', 'day', output_field=DateField())).values('Date_group',)
        semsterNumber = SubjectClass.objects.get(
            SubjectId=subjectId)
        subjectName = Subject.objects.get(id=subjectId)
        sectionName = Section.objects.get(id=SecId)
        date_list = []
        for x in dates:
            d = x.get('Date_group')
            d.isoformat()

            date_list.append(Attendance.objects.filter(Date=d)[0])
        date_list = list(dict.fromkeys(date_list))
        final_dates = [-1]*len(date_list)
        count = 0
        for x in date_list:
            final_dates[count] = [{'group': x}, {'TotalPresent': Attendance.objects.filter(
                Date=x.Date, SubjectId=subjectId, status=1).count()}]
            count = count+1
        classId = Section.objects.get(id=SecId).ClassId
        return Render.render('adminApp/subjectAtendance_report.html',  {'semsterId': semsterNumber, 'dates': final_dates,  'subjectId': subjectName, 'classId': classId, 'SectionId': sectionName})

    def subjectAttendance_view(self, request, SecId, SemsterId, subjectId):
        dates = Attendance.objects.annotate(Date_group=Trunc(
            'Date', 'day', output_field=DateField())).values('Date_group',)
        semsterNumber = SubjectClass.objects.get(
            SubjectId=subjectId)
        subjectName = Subject.objects.get(id=subjectId)
        sectionName = Section.objects.get(id=SecId)
        date_list = []
        for x in dates:
            d = x.get('Date_group')
            d.isoformat()

            date_list.append(Attendance.objects.filter(Date=d)[0])
        date_list = list(dict.fromkeys(date_list))
        final_dates = [-1]*len(date_list)
        count = 0
        for x in date_list:
            final_dates[count] = [{'group': x}, {'TotalPresent': Attendance.objects.filter(
                Date=x.Date, SubjectId=subjectId, status=1).count()}]
            count = count+1
        classId = Section.objects.get(id=SecId).ClassId
        return render(request, self.subjectAttendance_template, {'semsterId': semsterNumber, 'dates': final_dates,  'subjectId': subjectName, 'classId': classId, 'SectionId': sectionName})

    def markAttendance_view(self, request, SecId, SemsterId, subjectId):
        students = Student.objects.filter(SectionId=SecId)
        subject_id = Subject.objects.get(id=subjectId)
        if request.method == "POST":
            form = DateForm(request.POST)
            if form.is_valid():
                data = request.POST.copy()
                for x in students:
                    if data.get(x.registrationNumber):
                        c = Attendance(Date=data.get(
                            'date_Time'), StudentId=x, SubjectId=subject_id, status=True)
                        c.save()
                    else:
                        c = Attendance(Date=data.get(
                            'date_Time'), StudentId=x, SubjectId=subject_id, status=False)
                        c.save()

        classId = Section.objects.get(id=SecId).ClassId
        initial = {'date_Time': datetime.date.today}
        dateForm = DateForm(initial=initial)
        return render(request, self.markAttendance_template, {'semsterId': SemsterId, 'dateForm': dateForm, 'students': students, 'subjectId': subjectId, 'classId': classId, 'SectionId': SecId})

    def Evaluation_Report(Self, request, examId):
        exam_data = Exam.objects.get(id=examId)
        students = Student.objects.filter(SectionId=exam_data.SectionId)
        eval_data = []
        for y in students:
            isExist = list(Evaluation.objects.filter(
                ExamId=exam_data, StudentId=y))
            if isExist:
                eval_data.append(isExist)
        return Render.render('adminApp/EvaluationReport.html', {'exam_data': exam_data, 'students': eval_data})
    def StudentList_Report(Self, request, SecId):
        students = Student.objects.filter(SectionId=SecId)
        if len(students)>0:

            print(students[0].DepartmentId)
        return Render.render('adminApp/StudentReport.html', { 'classId':students[0].ClassId,'SectionId':students[0].SectionId,'DepartmentId':students[0].DepartmentId,'students': students})

    def markEvaluation_view(self, request, examId):
        exam_data = Exam.objects.get(id=examId)
        students = Student.objects.filter(SectionId=exam_data.SectionId)
        eval_data = []

        if request.method == "POST":
            data = request.POST.copy()
            for x in students:
                isExist = list(Evaluation.objects.filter(
                    ExamId=exam_data, StudentId=x))
                if not isExist:
                    setGrade = (int(data.get(x.registrationNumber))*100)/int(exam_data.totalMarks)
                    if setGrade > 85:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='A+', StudentId=x)
                    elif setGrade > 80:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='A', StudentId=x)
                    elif setGrade > 70:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='B+', StudentId=x)
                    elif setGrade > 60:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='B', StudentId=x)
                    elif setGrade > 50:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='C+', StudentId=x)
                    elif setGrade > 33:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='C-', StudentId=x)
                    else:
                        c = Evaluation(ExamId=exam_data, obtainedMarks=data.get(
                            x.registrationNumber), Grade='F', StudentId=x)
                    c.save()

            return redirect(reverse('admin:adminApp_section_change', args=(exam_data.SectionId.id,)))
        for y in students:
            isExist = list(Evaluation.objects.filter(
                ExamId=exam_data, StudentId=y))
            if isExist:
                eval_data.append(isExist)
        if len(eval_data) > 0:
            return render(request, self.updateEvaluation_template, {'exam_data': exam_data, 'students': eval_data})
        else:
            return render(request, self.markEvaluation_template, {'exam_data': exam_data, 'students': students})

    def sectionSubjects_view(self, request, SecId, SemsterId):
        sectionRequired = Section.objects.get(pk=SecId)
        subjects = SubjectClass.objects.filter(
            ClassId=sectionRequired.ClassId, DepartmentId=sectionRequired.DepartmentId, ProgramId=sectionRequired.ProgramId, SemsterName=SemsterId)
        return render(request, self.sectionSubjects_template, {'semsterId': SemsterId, 'SectionId': SecId, 'subjects': subjects})


class myClassAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    change_form_template = 'adminApp/changeClass.html'
    AddClassSubject_template = 'adminApp/addClassSubject.html'
    def get_urls(self):

        urls = super().get_urls()
        my_urls = [
            path('ClassSubject/<int:ClassId>', self.admin_site.admin_view(
                self.AddClassSubject_view), name='adminApp_class_subject')
        ]
        return my_urls + urls

    add_form_template = 'adminApp/addSection.html'
    def add_view(self, request, form_url='', extra_context=None):

        return super(myClassAdmin, self).add_view(request, form_url)

    def AddClassSubject_view(self, request, ClassId):
        if request.method == "POST":
            form = AddClassSubjectForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('admin:adminApp_class_change', args=(ClassId,)))
            else:
                return render(request, self.AddClassSubject_template, {'form': form, 'class_id': ClassId})
        else:
            Department_Id = Class.objects.get(id=ClassId).DepartmentId
            ProgramId_Id = Class.objects.get(id=ClassId).ProgramId
            initial = {'DepartmentId': Department_Id,
                       'ProgramId': ProgramId_Id, 'ClassId': ClassId}
            form = AddClassSubjectForm(initial=initial)
        return render(request, self.AddClassSubject_template, {'form': form, 'class_id': ClassId})

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        depId = Class.objects.get(pk=object_id).DepartmentId
        proId = Class.objects.get(pk=object_id).ProgramId
        extra_context['osm_data'] = Section.objects.filter(
            ClassId=object_id, DepartmentId=depId, ProgramId=proId)
        extra_context['subjects'] = SubjectClass.objects.filter(
            ClassId=object_id, DepartmentId=depId, ProgramId=proId)
        extra_context['class_id'] = object_id
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class myInstituteAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myStudentAdmin(admin.ModelAdmin):
    
    add_form_template = 'adminApp/addStudent.html'
    change_form_template = 'adminApp/changeStudent.html'
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    def get_fieldsets(self, request, obj=None):
        superclass = super(myStudentAdmin, self)
        fieldsets = superclass.get_fieldsets(request, obj)

        # Here we cycle through the fieldsets and remove the created and updated
        # fields by name. Factoring this out left as an exercise for the reader.
        for fs in fieldsets:
            fs[1]['fields'] = [f for f in fs[1]['fields']
                               if f not in self.hidden_fields]
        return fieldsets

    search_fields = ('registrationNumber', 'PersonId')
    list_filter = ('DepartmentId', 'SectionId', 'ClassId',)
    hidden_fields = ('PersonId')
    list_display = ('registrationNumber', 'PersonId', 'DepartmentId')

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == "POST":
            form = AddPersonForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = AddPersonForm(instance=None)
        return super(myStudentAdmin, self).add_view(request, form_url, {'form': form})

    def change_view(self,  request, object_id, form_url='', extra_context=None):
        if request.method == "POST":
            form = AddPersonForm(request.POST)
            if form.is_valid():
                form.save()
        else:

            c = Student.objects.get(id=object_id).PersonId
            change_Person = Person.objects.get(id=c.id)
            form = AddPersonForm(instance=change_Person)
        return super(myStudentAdmin, self).change_view(request, object_id, form_url, {'form': form})

    def save_model(self, request, obj, form, change):
        obj.PersonId = Person.objects.filter(
            Cnic=request.POST.get('Cnic')).reverse()[0]
        super().save_model(request, obj, form, change)

    def my_view(request):
        temResponse = add_view()
        return temResponse

    def my_view2(request):
        temResponse = change_view()
        return temResponse


class myPersonAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myEvaluationAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myLookupAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myEmplyeeAdmin(admin.ModelAdmin):

    add_form_template = 'adminApp/addEmployes.html'
    change_form_template = 'adminApp/teacherChange.html'
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    def get_fieldsets(self, request, obj=None):
        superclass = super(myEmplyeeAdmin, self)
        fieldsets = superclass.get_fieldsets(request, obj)

        # Here we cycle through the fieldsets and remove the created and updated
        # fields by name. Factoring this out left as an exercise for the reader.
        for fs in fieldsets:
            fs[1]['fields'] = [f for f in fs[1]['fields']
                               if f not in self.hidden_fields]
        return fieldsets

    hidden_fields = ('PersonId')

    def change_view(self,  request, object_id, form_url='', extra_context=None):
        if request.method == "POST":
            form = AddPersonForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            c = Employee.objects.get(id=object_id).PersonId
            change_Person = Person.objects.get(id=c.id)
            form = AddPersonForm(instance=change_Person)
            isTeacher = Employee.objects.get(id=object_id)
            if isTeacher.Designation != 5:
                notClerk = True
                courses = SubjectTeacher.objects.filter(TeacherId=isTeacher.id)
            else:
                notClerk = False
        return super(myEmplyeeAdmin, self).change_view(request, object_id, form_url, {'courses': courses, 'notClerk': notClerk, 'form': form})

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == "POST":
            form = AddPersonForm(request.POST)
            if form.is_valid():
                form.save()
        else:
            form = AddPersonForm(instance=None)
        return super(myEmplyeeAdmin, self).add_view(request, form_url, {'form': form})

    def save_model(self, request, obj, form, change):
        obj.PersonId = Person.objects.filter(
            Cnic=request.POST.get('Cnic')).reverse()[0]
        super().save_model(request, obj, form, change)

    def my_view(request):
        temResponse = add_view()
        return temResponse

    def my_view2(request):
        temResponse = change_view()
        return temResponse


class myExamAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class mySubjectTeacherAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class mySubjectAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myClassSubjectAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


admin.site.register(Institue, myInstituteAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, myProgramAdmin)
admin.site.register(Class, myClassAdmin)
admin.site.register(SubjectClass, myClassSubjectAdmin)

admin.site.register(Subject, mySubjectAdmin)
admin.site.register(Section, mySectionAdmin)
admin.site.register(Student, myStudentAdmin)
admin.site.register(Person, myPersonAdmin)
admin.site.register(Employee, myEmplyeeAdmin)
admin.site.register(Exam, myExamAdmin)


admin.site.register(Attendance, myAttendanceAdmin)
admin.site.register(Lookup, myLookupAdmin)
admin.site.register(Evaluation, myEvaluationAdmin)
admin.site.register(SubjectTeacher, mySubjectTeacherAdmin)
