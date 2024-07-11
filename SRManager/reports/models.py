from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from datetime import date
from django.utils import timezone

class CustomUser(AbstractUser,PermissionsMixin):
    ROLES={
        "ME":"Project Member",
        "PM":"Project Manager",
        "SA":"System Administrator"
    }
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=3,choices=ROLES)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ["username","first_name","last_name","role"]

class Projects(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    STATUS = [
        ("completed", "Completed"),
        ("progress", "In Progress"),
        ("start", "YET-TO START")
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now())
    taskDescription = models.TextField(default="Custom Description")
    accomplishments=models.TextField(blank=True)
    blockers=models.TextField(blank=True)
    document=models.FileField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default="start")

class Managers(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["manager", "project"], name="unique_manager_member"
            )
        ]
class Projectteams(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "member"], name="unique_project_member"
            )
        ]