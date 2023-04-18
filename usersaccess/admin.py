from django.contrib import admin
from .models import wills, ChangeLog, test
# Register your models here.


admin.site.register(wills)
admin.site.register(ChangeLog)
admin.site.register(test)