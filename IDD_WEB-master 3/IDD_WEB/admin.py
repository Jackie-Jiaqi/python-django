from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Register your models here.
admin.site.register(MongoConn)
admin.site.register(CSVConn)
admin.site.register(Author)