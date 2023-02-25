from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from Aca_sessions.models import Subjects

class Attendance_Student(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    session_name = models.CharField(verbose_name="Session ID",max_length=30)
    subject = models.PositiveSmallIntegerField(verbose_name="Subject",choices=Subjects.choices)
    present = models.BooleanField(verbose_name="Is Present",default=False)
    log_on_at = models.DateTimeField(verbose_name="Logged In At",null=True)
    log_out_at = models.DateTimeField(verbose_name="Logged Out At",null=True)
    total_duration = models.DurationField(verbose_name="Active duration",default=timedelta())
    active_user = models.BooleanField(verbose_name="Active Student",default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.session_name} | {Subjects.getting_label(self.subject)}"
# Create your models here.
