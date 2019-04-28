from django.apps import AppConfig


class AdminappConfig(AppConfig):
    name = 'adminApp'
"""
class Exam(models.Model):
    classSectionId = models.ForeignKey(classSection, on_delete=models.CASCADE)
    totalMarks = models.IntegerField()
    weightage = models.IntegerField()
    Name = models.CharField(max_length=12)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    Sub_Id = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

"""