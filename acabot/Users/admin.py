from django.contrib import admin
from Users.models import Students

class StudentAdmin(admin.ModelAdmin):
    pass

    def __str__(self) -> str:
        return self.user.username

admin.site.register(Students,StudentAdmin)

# Register your models here.
