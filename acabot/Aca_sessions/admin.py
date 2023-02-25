from django.contrib import admin
from Aca_sessions.models import Session_details
class SessionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Session_details,SessionsAdmin)
# Register your models here.
