from django.db import models


class Institue(models.Model):

    Name = models.CharField(max_length=60)
    Address = models.CharField(max_length=50)
    Contact = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Department(models.Model):
    InstitueId = models.ForeignKey(Institue,verbose_name="Institute", on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Contact = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Program(models.Model):
    Name = models.CharField("Program Name", max_length=20)
    DepartmentId = models.ForeignKey(Department,verbose_name="Department", on_delete=models.CASCADE)
    EntryTest = models.DateField("Entry Test")
    MeritList = models.DateField("Mert List")
    FeeSubmission = models.DateField("Fee Submission")
    ClassesCommence = models.DateField("Class Starts")

    def __str__(self):
        return self.Name

    class Meta:
        unique_together = (("Name", "DepartmentId"),)


class Lookup(models.Model):
    Value = models.CharField(max_length=20)
    Category = models.CharField(max_length=20)

    def __str__(self):
        return self.Value


class Class(models.Model):
    Name = models.CharField(max_length=20)
    DepartmentId = models.ForeignKey(Department,verbose_name="Department", on_delete=models.CASCADE)
    ProgramId = models.ForeignKey(Program, verbose_name="Program",on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Section(models.Model):

    DepartmentId = models.ForeignKey(
        Department, verbose_name="Department", on_delete=models.CASCADE)
    ProgramId = models.ForeignKey(
        Program, verbose_name="Program", on_delete=models.CASCADE)
    SectionName = models.CharField("Section", max_length=20)
    ClassId = models.ForeignKey(
        Class, verbose_name="Class", on_delete=models.CASCADE)
    Strength = models.IntegerField()

    def __str__(self):
        return self.SectionName



class Person(models.Model):
    FirstName = models.CharField("First Name", max_length=20)
    LastName = models.CharField("Last Name", max_length=20)
    FatherName = models.CharField("Father Name", max_length=30)
    Cnic = models.CharField("CNIC/B-FORM", max_length=20, unique=True)
    Address = models.CharField("Permenant Address", max_length=50)
    Contact = models.CharField("Phone Number", max_length=20)
    Gender = models.ForeignKey(Lookup, on_delete=models.CASCADE)

    def __str__(self):
        return self.FirstName+' '+self.LastName


class Student(models.Model):
    ClassId = models.ForeignKey(
        Class, verbose_name="Class", on_delete=models.CASCADE)
    SectionId = models.ForeignKey(
        Section, verbose_name="Section", on_delete=models.CASCADE)
    DepartmentId = models.ForeignKey(
        Department, verbose_name="Department", on_delete=models.CASCADE)
    ProgramId = models.ForeignKey(
        Program, verbose_name="Program", on_delete=models.CASCADE)
    registrationNumber = models.CharField(
        "Registration Number", max_length=12, unique=True)
    monthlyFee = models.IntegerField()
    PersonId = models.ForeignKey(
        Person, verbose_name="Name", on_delete=models.CASCADE)

    def __str__(self):
        return self.registrationNumber


Employess_CHOICES = ((1, 'Chair Person'), (2, 'Associate Professor'),
                     (3, 'Asistant Professor'), (4, 'Professor'), (5, 'Clerk'))


class Employee(models.Model):
    DepartmentId = models.ForeignKey(
        Department, verbose_name="Department", on_delete=models.CASCADE)
    PersonId = models.ForeignKey(
        Person, verbose_name="Person", on_delete=models.CASCADE)
    Designation = models.IntegerField(choices=Employess_CHOICES)
    Salary = models.IntegerField("Monthly Salary")

    def __str__(self):
        return str(self.PersonId)


class Days(models.Model):
    DayName = models.CharField("Day of Week", max_length=10)
    DayNumber = models.IntegerField()

    def __str__(self):
        return self.DayName


class Calender(models.Model):
    date_Time = models.DateField("Date")

    def __str__(self):
        return self.date_Time


BOOL_CHOICES = ((True, 'Present'), (False, 'Absent'))


class Fine(models.Model):
    amount = models.IntegerField()
    personId = models.ForeignKey(Person, verbose_name="Person",on_delete=models.CASCADE)
    designation = models.ForeignKey(Lookup, on_delete=models.CASCADE)

    def __str__(self):
        return self.amount


class Subject(models.Model):
    Name = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    DepartmentId = models.ForeignKey(Department,verbose_name="Department", on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Attendance(models.Model):
    Date = models.DateField()
    StudentId = models.ForeignKey(Student,verbose_name="Student", on_delete=models.CASCADE)
    SubjectId = models.ForeignKey(Subject, verbose_name="Subject",on_delete=models.CASCADE)
    status = models.BooleanField(choices=BOOL_CHOICES)

    def __str__(self):
        return str(self.Date)

    class Meta:
        unique_together = (("Date", "StudentId", "SubjectId"),)


class Exam(models.Model):

    Name = models.CharField(max_length=12)
    DepartmentId = models.ForeignKey(Department,verbose_name="Department", on_delete=models.CASCADE)
    ClassId = models.ForeignKey(Class, verbose_name="Class",on_delete=models.CASCADE)
    SectionId = models.ForeignKey(Section,verbose_name="Section", on_delete=models.CASCADE)
    SubjectId = models.ForeignKey(Subject,verbose_name="Subject", on_delete=models.CASCADE)
    totalMarks = models.IntegerField()
    weightage = models.IntegerField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()

    def __str__(self):
        return self.Name



class Evaluation(models.Model):
    ExamId = models.ForeignKey(Exam, verbose_name="Exam",on_delete=models.CASCADE)
    obtainedMarks = models.IntegerField()
    Grade = models.CharField(max_length=2)
    StudentId = models.ForeignKey(Student, verbose_name="Student",on_delete=models.CASCADE)
    class Meta:
        unique_together = (( "ExamId", "StudentId"),)


class SubjectClass(models.Model):
    DepartmentId = models.ForeignKey(Department,verbose_name="Department", on_delete=models.CASCADE)
    ProgramId = models.ForeignKey(Program,verbose_name="Program", on_delete=models.CASCADE)
    ClassId = models.ForeignKey(Class, verbose_name="Class",on_delete=models.CASCADE)
    SubjectId = models.ForeignKey(Subject,verbose_name="Subject", on_delete=models.CASCADE)
    SemsterName = models.CharField(max_length=10)

    def __str__(self):
        return self.SubjectId.Name

    class Meta:
        unique_together = (("ClassId", "SubjectId", "SemsterName"),)


class SubjectTeacher(models.Model):
    SubjectId = models.ForeignKey(
        Subject, on_delete=models.CASCADE)
    TeacherId = models.ForeignKey(
        Employee, on_delete=models.CASCADE)
    SectionId = models.ForeignKey(Section, on_delete=models.CASCADE)


class Period(models.Model):
    startTime = models.TimeField()
    EndTime = models.TimeField()
    periodNumber = models.IntegerField(primary_key=True)


class Scheduale(models.Model):
    dayName = models.ForeignKey(Days, on_delete=models.CASCADE)
    periodNumber = models.ForeignKey(Period, on_delete=models.CASCADE)
    SubjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)


class TimeTable(models.Model):
    SchedualeId = models.ForeignKey(Scheduale, on_delete=models.CASCADE)
    SubjectId = models.ForeignKey(Subject, on_delete=models.CASCADE)
    periodNumber = models.ForeignKey(Period, on_delete=models.CASCADE)
    TeacherId = models.ForeignKey(Employee, on_delete=models.CASCADE)
    SchedualeDateAndTime = models.ForeignKey(
        Calender, on_delete=models.CASCADE)
