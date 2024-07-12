from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from .models import Tasks,Managers,Projectteams,Projects,CustomUser
from .forms import Taskform
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.

def teamMembers(request,project):
    members={}
    members[request.user.id]=request.user.first_name+" "+request.user.last_name
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
        projects={}
        managerObj=list(Managers.objects.filter(manager=request.user.id).select_related("project"))
        projects[managerObj[0].project.id]=managerObj[0].project.name
        return projects

def allUsers():
    employees={}
    employeesList=list(CustomUser.objects.filter(~Q(role="SA")))
    for employee in employeesList:
        employees[employee.id]=employee.first_name+" "+employee.last_name
    return employees

def projectsList():
    projects={}
    for project in list(Projects.objects.all()):
        projects[project.id]=project.name
    return projects

def loginUser(request):
    if request.method=="POST":
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            if(request.user.role=="SA"):
                employees=allUsers()
                projects=projectsList()
                request.session["employees"]=employees
                request.session["projects"]=projects
                return redirect("/executive/")
            projects=projectsDict(request)
            request.session["projects"]=projects
            if(request.user.role=="PM"):
                members=teamMembers(request,list(projects.keys())[0])
                request.session["members"]=members
            return redirect("/viewTasks/")
        else:
            error=form.errors.as_text()
            return render(request,"login.html",{"error":error})
    if request.user.is_authenticated:
        if request.user.role=="SA":
            return redirect("/executive/")
        return redirect("/viewTasks")
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
                return render(request,"members/createTask.html",{"projects":request.session["projects"],"errors":form.errors.as_text()})
        return render(request,"members/createTask.html",{"projects":request.session["projects"]})
   
    else:
        if request.method=="POST":
            form=Taskform(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect("/viewTasks/")
            else:
                return render(request,"manager/createTask.html",{"project":list(request.session["projects"].keys())[0],"errors":form.errors.as_text()})
        return render(request,"manager/createTask.html",{"project":request.session["projects"]})


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
            tasks=list(Tasks.objects.filter(user=request.user.id,).select_related("project"))
        return render(request,"manager/viewTasks.html",{"tasks":tasks,"projects":request.session["projects"],"members":request.session["members"]})
    
@login_required(login_url="/login")
def memebersTasks(request):
    if request.user.role=="PM":
        if request.method=="POST":
            date=request.POST["date"]
            project=list(request.session["projects"].keys())[0]
            if date:
                tasks=Tasks.objects.filter(date=date,project=project).select_related("user")
            else:
                tasks=Tasks.objects.filter(project=project).select_related("user")
        else:
            project=list(request.session["projects"].keys())[0]
            tasks=Tasks.objects.filter(project=project).select_related("user")
        return render(request,"manager/membersTasks.html",{"tasks":tasks,"projects":request.session["projects"],"members":request.session["members"]})
    else:
        return redirect("/viewTasks")
    
@login_required(login_url="/login")
def memberTasks(request,userid):
    if request.user.role=="PM":
        if request.method=="POST":
            date=request.POST["date"]
            project=list(request.session["projects"].keys())[0]
            if date:
                tasks=Tasks.objects.filter(user=userid,date=date,project=project).select_related("user")
            else:
                tasks=Tasks.objects.filter(user=userid,project=project).select_related("user")
        else:
            project=list(request.session["projects"].keys())[0]
            tasks=list(Tasks.objects.filter(user=userid,project=project).select_related("user"))
        return render(request,"manager/membersTasks.html",{"tasks":tasks,"projects":request.session["projects"],"members":request.session["members"]})
    else:
        return redirect("/viewTasks")


@login_required(login_url="/login/")
def executive(request):
    if request.user.role=="SA":
        if request.method=="POST":
            date=request.POST["date"]
            project=request.POST["project"]
            if not date and project:
                tasks=list(Tasks.objects.filter(project=project).select_related("project"))
            elif date and not project:
                tasks=list(Tasks.objects.filter(date=date).select_related("project"))
            elif date and project:
                tasks=list(Tasks.objects.filter(project=project,date=date).select_related("project"))
            else:
                tasks=list(Tasks.objects.filter().select_related("project"))
        else:
            tasks=Tasks.objects.all().select_related("project")
        return render(request,"executive/viewTasks.html",{"employees":request.session["employees"],"tasks":tasks,"projects":request.session["projects"]})
    else:
        return redirect("/viewTasks")

@login_required(login_url="/login/")
def executiveMemberTasks(request,userid):
    if request.user.role=="SA":
        if request.method=="POST":
            date=request.POST["date"]
            project=request.POST["project"]
            if not date and project:
                tasks=list(Tasks.objects.filter(user=userid,project=project).select_related("project"))
            elif date and not project:
                tasks=list(Tasks.objects.filter(user=userid,date=date).select_related("project"))
            elif date and project:
                tasks=list(Tasks.objects.filter(user=userid,project=project,date=date).select_related("project"))
            else:
                tasks=list(Tasks.objects.filter(user=userid).select_related("project"))
        else:
            tasks=Tasks.objects.filter(user=userid).select_related("project")
        return render(request,"executive/viewTasks.html",{"employees":request.session["employees"],"tasks":tasks,"projects":request.session["projects"]})
    else:
        return redirect("/viewTasks/")

@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("/login/")