from django.db import models
from Aca_sessions.models import Subjects,Session_details


class Homeworks(models.Model):
    name = models.CharField(max_length=20,verbose_name="Home Work name")
    session = models.ForeignKey(Session_details,on_delete=models.CASCADE)
    subject = models.PositiveSmallIntegerField(verbose_name="Subject",choices=Subjects.choices)
    deadline = models.DateTimeField(verbose_name="Deadline")
    no_of_students_done_before_deadline = models.PositiveSmallIntegerField(verbose_name="How many students done before deadline",default=0)
    no_of_students_done_after_deadline = models.PositiveSmallIntegerField(verbose_name="How many students done after deadline",default=0)


    def __str__(self) -> str:
        return f"{Subjects.getting_label(self.subject)} - {self.name}"

