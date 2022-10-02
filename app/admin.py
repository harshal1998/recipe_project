from django.contrib import admin
from . models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['name', 'email', 'username']

@admin.register(Receipies)
class ReceipiesAdmin(admin.ModelAdmin):
    model = Receipies
    list_display = ['added_by','name']