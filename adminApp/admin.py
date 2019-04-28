
from django.template.response import TemplateResponse
from django.contrib import admin
from django.urls import reverse
from django.urls import resolve, path
from django.utils.html import format_html
from .models import Institue, Department, Program, Class, Section, Student, Person, Employee, Exam, Lookup
# Register your models here.
from django.forms.models import BaseInlineFormSet
admin.site.site_header = 'Learning Managemnet System'

admin.site.site_title = 'LMS'

admin.site.index_title = 'Admin'
"""
class ChildInlineFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(ChildInlineFormSet, self).__init__(*args, **kwargs)
        primeKey = self.instance.pk
        DepartmentKey = self.instance.DepartmentId.id
        # Now we need to make a queryset to each field of each form inline
        depId = Program.objects.filter(id=DepartmentKey)
        print(depId)
        self.queryset = Class.objects.filter(DepartmentId=6)

"""


class ClassInline(admin.TabularInline):
    model = Class
    list_display_links = ('Name')
    extra = 0
    """
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print('qqqqqqqqqqqqqq')
        if db_field.name == "DepartmentId":
            print('jjjhj')
            parent_obj_id = kwargs.get('id')
            kwargs["queryset"] = Class.objects.filter(
                ProgramId=parent_obj_id,Name='2018')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        try:
            self.fields['DepartmentId'].queryset = Department.objects.filter(
                pk=self.instance.DepartmentId)
        except:
            self.fields['DepartmentId'].queryset = Department.objects
        return super(PictureInline, self).formfield_for_foreignkey(db_field, request=None, **kwargs)

    def get_formset(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(
            self.formfield_for_dbfield, request=request, obj=obj)
        return super().get_formset(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        obj = kwargs.pop('obj', None)
        print('qqqqqqqqqqqqqq')
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "DepartmentId":
            print('jjjhj')
            formfield.queryset = Class.objects.filter(
                ProgramId=parent_obj_id,Name='2018')
        return formfield

    def get_parent_object_from_request(self, request):
        resolved = resolve(request.path_info)
        if resolved.kwargs.get('id'):
            print(resolved.kwargs.get('DepartmentId'))
            print('jjnjn')
            return self.parent_model.objects.get(DepartmentId=resolved.args[6])
        print('jjnjnsssssssssssssss')
        return None

    def has_add_permission(self, request):
        parent = self.get_parent_object_from_request(request)
        if parent:
            return parent.status == 1
        return super(ClassInline, self).has_add_permission(request)


    def get_queryset(self,request):
        qs=super(ClassInline,self).get_queryset(request)

        print('HHHH')
        print('ndsm,dm'+request.data)
        return qs.filter(ProgramId=request1.id)


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "Name":
            kwargs["queryset"] = Name.objects.filter(
                DepartmentId=7,ProgramId=6)
        elif db_field.name == "DepartmentId":
            kwargs["queryset"] = DepartmentId.objects.filter(
                DepartmentId=7,ProgramId=6)
        elif db_field.name == "ProgramId":
            kwargs["queryset"] = ProgramId.objects.filter(
                DepartmentId=7,ProgramId=6)
        return super(ClassInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
    """


class SectionInline(admin.TabularInline):

    model = Section
    extra = 0


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
    inlines = [ProgramInline]
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
    """
    def change_view(self, request, object_id, extra_context=None):
        print('qaim')
        print('sanan')
        print(object_id)

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'ProgramId':

                print('jhjhjhjhjhhhjhjh')
                depId = Program.objects.get(pk=object_id).DepartmentId
                kwargs['queryset'] = Class.objects.filter(
                    ProgramId=object_id, DepartmentId=depId)
            return super(ClassInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        ClassInline.formfield_for_foreignkey = formfield_for_foreignkey

        self.inline_instances = [ClassInline(self.model, self.admin_site)]

        return super(myProgramAdmin, self).change_view(request, object_id,
                                                       extra_context=extra_context)



    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'ProgramId':
            print('knssjkjskjkj')
            depId = Program.objects.get(pk=object_id).DepartmentId
            kwargs['queryset'] = Class.objects.filter(
                ProgramId=object_id, DepartmentId=depId)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    """


class mySectionAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myClassAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    change_form_template = 'adminApp/changeClass.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        print(object_id)
        depId = Class.objects.get(pk=object_id).DepartmentId
        extra_context['osm_data'] = Section.objects.filter(
            ClassId=object_id, DepartmentId=depId)
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
    def add_view(self, request,form_url='', extra_context=None):
        
        if request.method == "POST":
            fname = request.POST.get('FirstName')
            lname = request.POST.get('LastName')
            fatherName = request.POST.get('FatherName')
            cnic = request.POST.get('Cnic')
            address = request.POST.get('Address')
            contactNumber = request.POST.get('Contact')
            gender = Lookup.objects.get(Value='Male')
            pId = Person(FirstName=fname, LastName=lname, FatherName=fatherName,
                       Cnic=cnic, Address=address, Contact=contactNumber, Gender=gender)
            pId.save()
        return super(myStudentAdmin, self).add_view(request)

    def my_view(request):
        temResponse = add_view()
        return temResponse


class myPersonAdmin(admin.ModelAdmin):
    pass


class myEmplyeeAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class myExamAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


admin.site.register(Institue, myInstituteAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, myProgramAdmin)
admin.site.register(Class, myClassAdmin)
admin.site.register(Section, mySectionAdmin)
admin.site.register(Student, myStudentAdmin)
admin.site.register(Person, myPersonAdmin)
admin.site.register(Employee, myEmplyeeAdmin)
admin.site.register(Exam, myExamAdmin)

admin.site.register(Lookup)
