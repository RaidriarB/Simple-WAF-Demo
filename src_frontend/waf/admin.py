from django.contrib import admin
from .models import Rule,Log,Fulllog
# Register your models here.

admin.site.register(Rule)
admin.site.register(Log)
admin.site.register(Fulllog)