from django.contrib import admin
from .models import wills, ChangeLog, test, TestChange, UserProfile
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


admin.site.register(wills)
admin.site.register(ChangeLog)
admin.site.register(test)
admin.site.register(TestChange, SimpleHistoryAdmin)
admin.site.register(UserProfile)
