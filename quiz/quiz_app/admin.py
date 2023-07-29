from django.contrib import admin
from .models import Answer,Response,Question
# Register your models here.
class ResponseAdmin(admin.ModelAdmin):
    list_display=('user','question','user_response')
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Response,ResponseAdmin)