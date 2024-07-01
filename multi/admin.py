from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(KycUser)
class KycUserAdmin(admin.ModelAdmin):
    list_display = ('doc_type','doc_img','user_id')