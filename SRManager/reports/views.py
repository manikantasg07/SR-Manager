from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .models import Tasks,Managers,Projectteams,Projects
from .forms import Taskform
from django.http import HttpResponse
# Create your views here.

def teamMembers(request):
    members={}
    managerObj=list(Managers.objects.filter(manager=request.user.id).select_related("project"))
    project=managerObj[0].project.id
    teamMembers=list(Projectteams.objects.filter(project=project).select_related("member"))
    for member in teamMembers:
        members[member.member.id]=member.member.first_name+" "+member.member.last_name
    return members


def projectsDict(request):
    if request.user.role=="ME":
        projectteams=Projectteams.objects.filter(member=request.user.id).select_related("project")
        projects={}
        for object in projectteams:
            projects[object.project.id]=object.project.name
        return projects
    else:
        project={}
        managerObj=list(Managers.objects.filter(manager=request.user.id).select_related("project"))
        project[managerObj[0].project.id]=managerObj[0].project.name


def loginUser(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            projects=projectsDict(request)
            request.session["projects"]=projects
            return redirect("/viewTasks/")
        else:
            error=form.errors.as_text()
            return render(request,"login.html",{"error":error})
    return render(request,"login.html")

@login_required(login_url="/login")
def createtask(request):
    if request.user.role=="ME":
        if request.method=="POST":
            form=Taskform(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect("/viewTasks/")
            else:
                return HttpResponse(form.errors.as_json())
        return render(request,"members/createTask.html",{"projects":request.session["projects"]})
    else:
        if request.method=="POST":
            form=Taskform(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect("/viewTasks/")
            else:
                return HttpResponse(form.errors.as_json())
        return render(request,"manager/createTask.html",{"projects":request.session["projects"]})


@login_required(login_url="/login")
def viewTasks(request):
    if request.user.role=="ME":
        if request.method=="POST":
            date=request.POST["date"]
            project=request.POST["project"]
            if not date and project:
                tasks=list(Tasks.objects.filter(user=request.user.id,project=project).select_related("project"))
            elif date and not project:
                tasks=list(Tasks.objects.filter(user=request.user.id,date=date).select_related("project"))
            elif date and project:
                tasks=list(Tasks.objects.filter(user=request.user.id,project=project,date=date).select_related("project"))
            else:
                tasks=list(Tasks.objects.filter(user=request.user.id).select_related("project")) 
        else:
            tasks=list(Tasks.objects.filter(user=request.user.id).select_related("project"))
        return render(request,"members/viewTasks.html",{"tasks":tasks,"projects":request.session["projects"]})
    else:
        tasks=list(Tasks.objects.filter(user=request.user.id).select_related("project"))
        return render(request,"manager/viewTasks.html",{"tasks":tasks,"projects":request.session["projects"]})

@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("/login/")