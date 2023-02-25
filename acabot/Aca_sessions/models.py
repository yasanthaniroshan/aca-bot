from django.db import models

class Subjects(models.IntegerChoices):
    Maths = 1 , "Mathematics",
    CS = 2 , "CS",
    Fluid = 3 , "Fluid Mechanic",
    Electrical = 4 , "Elcetrical Fundementals",
    Material = 5 , "Properties of Materials",
    Mechanics = 6 , "Mechanics",

    def getting_label(integer):
        integer = int(integer)
        if Subjects.Maths.value == integer:
            return Subjects.Maths.name
        elif Subjects.CS.value == integer:
            return Subjects.CS.name
        elif Subjects.Fluid.value == integer:
            return Subjects.Fluid.name
        elif Subjects.Electrical.value == integer:
            return Subjects.Electrical.name
        elif Subjects.Material.value == integer:
            return Subjects.Material.name
        elif Subjects.Mechanics.value == integer:
            return Subjects.Mechanics.name
        else:
            return None

class Session_details(models.Model):
    name = models.CharField(verbose_name="Session ID",max_length=20)
    subject = models.PositiveSmallIntegerField(verbose_name="Module",choices=Subjects.choices)
    started_at = models.DateTimeField(verbose_name="Started At",blank=True)
    ended_at = models.DateTimeField(verbose_name="Ended At",blank=True,null=True)
    no_of_students_at_started = models.PositiveSmallIntegerField(verbose_name="How many students were in Starting",default=0)
    no_of_students_at_ended = models.PositiveSmallIntegerField(verbose_name="How many students were in Ending",default=0)
    total_time = models.DurationField(verbose_name="Session Duration",blank=True,null=True)
    started = models.BooleanField(verbose_name="Is Started",default=False,null=True)
    ended = models.BooleanField(verbose_name="Is Ended",default=False,null=True)

    def __str__(self) -> str:
        return f"{Subjects.getting_label(self.subject)} - {self.name}"
# Create your models here.
