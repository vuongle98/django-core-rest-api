from django.contrib import admin

from menu.models import MenuItem


# Register your models here.

@admin.register(MenuItem)
class MenuAdmin(admin.ModelAdmin):
    pass