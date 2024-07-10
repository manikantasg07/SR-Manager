from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Tasks,Projects,Managers,CustomUser,Projectteams
from .forms import Userform,Managerform,Taskform,Memberform

class Accountadmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ("username",'email', 'first_name', 'last_name', 'password1', 'password2',"role"),
            },
        ),
    )

class Manageradmin(admin.ModelAdmin):
    form=Managerform

class Memberadmin(admin.ModelAdmin):
    form=Memberform

admin.site.register(CustomUser,Accountadmin)
admin.site.register(Managers,Manageradmin)
admin.site.register(Tasks)
admin.site.register(Projects)
admin.site.register(Projectteams,Memberadmin)