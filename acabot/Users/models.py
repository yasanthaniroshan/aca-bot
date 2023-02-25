from django.db import models
from django.contrib.auth.models import User

class Students(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    island_rank = models.CharField(max_length=4,verbose_name="Island Rank",blank=True)
    school = models.CharField(max_length=30,verbose_name="School",blank=True)
    whatsapp_number = models.CharField(max_length=12,verbose_name="Whataspp Number",blank=True)
    registered = models.BooleanField(verbose_name="Is Registered Student",default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.user.first_name}"
# Create your models here.
