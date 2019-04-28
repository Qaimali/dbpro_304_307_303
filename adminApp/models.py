from django.db import models


class Institue(models.Model):

    Name = models.CharField(max_length=60)
    Address = models.CharField(max_length=50)
    Contact = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Department(models.Model):
    InstitueId = models.ForeignKey(Institue, on_delete=models.CASCADE)
    Name = models.CharField(max_length=60)
    Contact = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Program(models.Model):
    Name = models.CharField("Program Name", max_length=20)
    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
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
    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    ProgramId = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Section(models.Model):

    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    SectionName = models.CharField("Section", max_length=20)
    ClassId = models.ForeignKey(
        Class, on_delete=models.CASCADE)
    Strength = models.IntegerField()
    registered = models.IntegerField()

    def __str__(self):
        return self.SectionName

    class Meta:
        unique_together = (("SectionName", "ClassId"),)


class classSection(models.Model):

    ClassId = models.ForeignKey(
        Class, on_delete=models.CASCADE)
    SectionId = models.ForeignKey(
        Section, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("ClassId", "SectionId"),)

class Person(models.Model):
    FirstName = models.CharField("First Name", max_length=20)
    LastName = models.CharField("Last Name", max_length=20)
    FatherName = models.CharField("Father Name", max_length=30)
    Cnic = models.CharField("CNIC/B-FORM", max_length=20)
    Address = models.CharField("Permenant Address", max_length=50)
    Contact = models.CharField("Phone Number", max_length=20)
    Gender = models.ForeignKey(Lookup, on_delete=models.CASCADE)

    def __str__(self):
        return self.FirstName+self.LastName
class Student(models.Model):
    ClassId = models.ForeignKey(
        Class, on_delete=models.CASCADE)
    SectionId = models.ForeignKey(
        Section, on_delete=models.CASCADE)
    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    registrationNumber = models.CharField(max_length=12,unique=True)
    monthlyFee = models.IntegerField()
    PersonId=models.ForeignKey(Person,on_delete=models.CASCADE)
    def __str__(self):
        return self.registrationNumber






class Employee(models.Model):
    DepartmentId = models.ForeignKey(Department, on_delete=models.CASCADE)
    PersonId = models.ForeignKey(Person, on_delete=models.CASCADE)
    Batch = models.DateField()
    Designation = models.ForeignKey(Lookup, on_delete=models.CASCADE)
    Salary = models.IntegerField("Monthly Salary")


class Days(models.Model):
    DayName = models.CharField("Day of Week", max_length=10)
    DayNumber = models.IntegerField()

    def __str__(self):
        return self.DayName


class Calender(models.Model):
    date_Time = models.DateTimeField()
    DayName = models.ForeignKey(Days, on_delete=models.CASCADE)

    def __str__(self):
        return self.DayName+self.date_Time


BOOL_CHOICES = ((True, 'Present'), (False, 'Absent'))


class Attendance(models.Model):
    Date = models.DateTimeField()
    personId = models.ForeignKey(Person, on_delete=models.CASCADE)
    designaion = models.ForeignKey(Lookup, on_delete=models.CASCADE)
    status = models.BooleanField(choices=BOOL_CHOICES)

    def __str__(self):
        return self.status


class Fine(models.Model):
    amount = models.IntegerField()
    personId = models.ForeignKey(Person, on_delete=models.CASCADE)
    designation = models.ForeignKey(Lookup, on_delete=models.CASCADE)

    def __str__(self):
        return self.amount


class Subject(models.Model):
    Name = models.CharField(max_length=15)
    description = models.CharField(max_length=255)
    ProgramId = models.ForeignKey(Program, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Exam(models.Model):
    classSectionId = models.ForeignKey(classSection, on_delete=models.CASCADE)
    totalMarks = models.IntegerField()
    weightage = models.IntegerField()
    Name = models.CharField(max_length=12)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    Subject_Id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name


class Result(models.Model):
    classSectionId = models.ForeignKey(classSection, on_delete=models.CASCADE)
    ExamId = models.ForeignKey(Exam, on_delete=models.CASCADE)
    minRange = models.IntegerField()
    maxRange = models.IntegerField()
    Grade = models.CharField(max_length=2)


class Evaluation(models.Model):
    Result = models.ForeignKey(Result, on_delete=models.CASCADE)
    obtainedMarks = models.IntegerField()
    Grade = models.CharField(max_length=2)
    StudentId = models.ForeignKey(Student, on_delete=models.CASCADE)


class SubjectTeacher(models.Model):
    SubjectId = models.ForeignKey(
        Subject, on_delete=models.CASCADE)
    TeacherId = models.ForeignKey(
        Employee, on_delete=models.CASCADE)
    classSectionId = models.ForeignKey(
        classSection, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("classSectionId", "TeacherId", "SubjectId"),)


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
