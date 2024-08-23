from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Tasks, Managers, Projectteams, Projects, CustomUser
from .forms import Taskform, Userform, Projectform, Memberform
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, date
import json
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404

# Create your views here.

def teamMembers(request, project):
    members = {}
    members[request.user.id] = request.user.first_name + " " + request.user.last_name
    teamMembers = list(Projectteams.objects.filter(project=project).select_related("member"))
    for member in teamMembers:
        members[member.member.id] = member.member.first_name + " " + member.member.last_name
    return members


def projectsDict(request):
    if request.user.role == "ME":
        projectteams = Projectteams.objects.filter(member=request.user.id).select_related("project")
        projects = {}
        for object in projectteams:
            projects[object.project.id] = object.project.name
        return projects
    else:
        projects = {}
        managerObj = list(Managers.objects.filter(manager=request.user.id).select_related("project"))
        projects[managerObj[0].project.id] = managerObj[0].project.name
        return projects


def allUsers():
    employees = {}
    employeesList = list(CustomUser.objects.filter())
    for employee in employeesList:
        employees[employee.id] = [employee.first_name + " " + employee.last_name,employee.role]
    return employees


def projectsList():
    projects = {}
    for project in list(Projects.objects.all()):
        projects[project.id] = project.name
    return projects


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.user.is_superuser:
                return redirect("/users/")
            elif (request.user.role == "SA"):
                employees = allUsers()
                projects = projectsList()
                request.session["employees"] = employees
                request.session["projects"] = projects
                return redirect("/executive/")
            projects = projectsDict(request)
            request.session["projects"] = projects
            if (request.user.role == "PM"):
                members = teamMembers(request, list(projects.keys())[0])
                request.session["members"] = members
            return redirect("/viewTasks/")
        else:
            error = form.errors
            return render(request, "login.html", {"error": error})
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/addUser/")
        elif request.user.role == "SA":
            return redirect("/executive/")
        return redirect("/viewTasks")
    return render(request, "login.html")


def save_files(request):
    try:
        file_names = ""
        files = request.FILES.getlist('document')
        file_paths = []

        for file in files:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_paths.append(filename)

        if file_paths:
            file_names += ','.join(file_paths)

        return file_names
    except:
        return ""


@login_required(login_url="/login")
def createtask(request):
    try:
        try:
            if date.today() < datetime.strptime(request.POST["date"], '%Y-%m-%d').date():
                return render(request, "members/createTask.html",
                              {"projects": request.session["projects"],
                               "errors": "Sorry you cannot add Task for a future date..<br> Please try with todays date..!"})
        except:
            pass
        if request.user.role == "ME":
            if request.method == "POST":
                form = Taskform(request.POST, request.FILES)
                if form.is_valid():
                    task = form.save(commit=False)
                    task.documents = save_files(request)
                    task.save()
                    return redirect("/viewTasks/")
                else:
                    return render(request, "members/createTask.html",
                                  {"projects": request.session["projects"], "errors": form.errors})
            return render(request, "members/createTask.html", {"projects": request.session["projects"]})

        else:
            if request.method == "POST":
                form = Taskform(request.POST, request.FILES)
                if form.is_valid():
                    task = form.save(commit=False)
                    task.documents = save_files(request)
                    task.save()
                    return redirect("/viewTasks/")
                else:
                    return render(request, "manager/createTask.html",
                                  {"project": list(request.session["projects"].keys())[0], "errors": form.errors})
            return render(request, "manager/createTask.html", {"project": request.session["projects"]})
    except Exception as e:
        return render(request, "members/createTask.html", {"projects": request.session["projects"], "errors": e})


@login_required(login_url="/login")
def viewTasks(request):
    errors=""
    try:
        errors = request.session["error"]
        print(errors)
        del request.session["error"]
    except:
        pass
    if request.user.role == "ME":
        if request.method == "POST":
            date = request.POST["date"]
            project = request.POST["project"]
            if not date and project:
                tasks = list(Tasks.objects.filter(user=request.user.id, project=project).select_related("project"))
            elif date and not project:
                tasks = list(Tasks.objects.filter(user=request.user.id, date=date).select_related("project"))
            elif date and project:
                tasks = list(
                    Tasks.objects.filter(user=request.user.id, project=project, date=date).select_related("project"))
            else:
                tasks = list(Tasks.objects.filter(user=request.user.id).select_related("project"))
        else:
            tasks = list(Tasks.objects.filter(user=request.user.id).select_related("project"))
        return render(request, "members/viewTasks.html", {"tasks": tasks, "projects": request.session["projects"],"errors":errors})
    else:
        if request.method == "POST":
            date = request.POST["date"]
            project = request.POST["project"]
            if not date and project:
                tasks = list(Tasks.objects.filter(user=request.user.id, project=project).select_related("project"))
            elif date and not project:
                tasks = list(Tasks.objects.filter(user=request.user.id, date=date).select_related("project"))
            elif date and project:
                tasks = list(
                    Tasks.objects.filter(user=request.user.id, project=project, date=date).select_related("project"))
            else:
                tasks = list(Tasks.objects.filter(user=request.user.id).select_related("project"))
        else:
            tasks = list(Tasks.objects.filter(user=request.user.id, ).select_related("project"))

        return render(request, "manager/viewTasks.html",
                      {"tasks": tasks, "projects": request.session["projects"], "members": request.session["members"],"errors":errors})


@login_required(login_url="/login/")
def viewSpeficTask(request, taskId):
    tasks = Tasks.objects.filter(id=taskId).select_related("project")
    data = {}
    for task in tasks:
        data["project"] = task.project.name
        data["date"] = task.date.strftime('%m/%d/%Y')
        data["taskDescription"] = task.taskDescription
        data["accomplishments"] = task.accomplishments
        data["blockers"] = task.blockers
        data["documents"] = task.documents
        data["status"] = task.status
    return HttpResponse(json.dumps(data))


@login_required(login_url="/login")
def memebersTasks(request):
    if request.user.role == "PM":
        if request.method == "POST":
            date = request.POST["date"]
            project = list(request.session["projects"].keys())[0]
            if date:
                tasks = Tasks.objects.filter(date=date, project=project).select_related("user")
            else:
                tasks = Tasks.objects.filter(project=project).select_related("user")
        else:
            project = list(request.session["projects"].keys())[0]
            tasks = Tasks.objects.filter(project=project).select_related("user")
        return render(request, "manager/membersTasks.html",
                      {"tasks": tasks, "projects": request.session["projects"], "members": request.session["members"]})
    else:
        return redirect("/viewTasks")


@login_required(login_url="/login")
def memberTasks(request, userid):
    if request.user.role == "PM":
        if request.method == "POST":
            date = request.POST["date"]
            project = list(request.session["projects"].keys())[0]
            if date:
                tasks = Tasks.objects.filter(user=userid, date=date, project=project).select_related("user")
            else:
                tasks = Tasks.objects.filter(user=userid, project=project).select_related("user")
        else:
            project = list(request.session["projects"].keys())[0]
            tasks = list(Tasks.objects.filter(user=userid, project=project).select_related("user"))
        return render(request, "manager/membersTasks.html",
                      {"tasks": tasks, "projects": request.session["projects"], "members": request.session["members"]})
    else:
        return redirect("/viewTasks")


@login_required(login_url="/login/")
def executive(request):
    if request.user.role == "SA":
        if request.method == "POST":
            date = request.POST["date"]
            project = request.POST["project"]
            if not date and project:
                tasks = list(Tasks.objects.filter(project=project).select_related("project"))
            elif date and not project:
                tasks = list(Tasks.objects.filter(date=date).select_related("project"))
            elif date and project:
                tasks = list(Tasks.objects.filter(project=project, date=date).select_related("project"))
            else:
                tasks = list(Tasks.objects.filter().select_related("project"))
        else:
            tasks = Tasks.objects.all().select_related("project")
        print(request.session["employees"])
        return render(request, "executive/viewTasks.html", {"employees": request.session["employees"], "tasks": tasks,
                                                            "projects": request.session["projects"]})
    else:
        return redirect("/viewTasks")


@login_required(login_url="/login/")
def executiveMemberTasks(request, userid):
    if request.user.role == "SA":
        if request.method == "POST":
            date = request.POST["date"]
            project = request.POST["project"]
            if not date and project:
                tasks = list(Tasks.objects.filter(user=userid, project=project).select_related("project"))
            elif date and not project:
                tasks = list(Tasks.objects.filter(user=userid, date=date).select_related("project"))
            elif date and project:
                tasks = list(Tasks.objects.filter(user=userid, project=project, date=date).select_related("project"))
            else:
                tasks = list(Tasks.objects.filter(user=userid).select_related("project"))
        else:
            tasks = Tasks.objects.filter(user=userid).select_related("project")
        return render(request, "executive/viewTasks.html", {"employees": request.session["employees"], "tasks": tasks,
                                                            "projects": request.session["projects"]})
    else:
        return redirect("/viewTasks/")


@login_required(login_url="/login/")
def employees(request):
    users = list(CustomUser.objects.all())
    return render(request, "administrator/employees.html", {"users": users})


@login_required(login_url="/login/")
def addUser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = Userform(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/users/")
            else:
                return render(request, "administrator/addUser.html", {"errors": form.errors})
        return render(request, "administrator/addUser.html")
    else:
        return HttpResponse("No permission to access")


@login_required(login_url="/login/")
def deleteUser(request, userId):
    try:
        CustomUser.objects.filter(id=userId).delete()
        return HttpResponse("User successfully Deleted")
    except:
        response = HttpResponse()
        response.status_code = 400
        response.reason_phrase = "No user with that id"
        return response


@login_required(login_url="/login/")
def addProject(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = Projectform(request.POST)
            if form.is_valid():
                form.save()
                return render(request, "administrator/addProject.html",
                              {"success": "Project has been succesfully created"})
            else:
                print(form.errors)
                return render(request, "administrator/addProject.html", {"errors": form.errors})
        return render(request, "administrator/addProject.html")
    else:
        return HttpResponse("No permission to access")


@login_required(login_url="/login/")
def viewSpeficUser(request, userId):
    if request.user.is_superuser:
        ROLES = {
            "ME": "Project Member",
            "PM": "Project Manager",
            "SA": "System Administrator"
        }
        user = CustomUser.objects.get(id=userId)
        data = {}
        data["username"] = user.username
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["email"] = user.email
        data["role"] = ROLES[user.role]
        data["role_value"] = user.role
        data["password"] = user.password

        data["projects"] = Projectteams.objects.filter(member=user).values_list('project', flat=True)
        data["projects"] = ", ".join((Projects.objects.filter(id__in=data["projects"]) | Projects.objects.filter(
            managers__manager=user)).values_list('name', flat=True))

        data["manager_names"] = ""
        data["project_members"] = ""

        if user.role == "ME":
            projects_user_is_in = Projectteams.objects.filter(member=user).values_list('project', flat=True)
            managers = Managers.objects.filter(project__in=projects_user_is_in).values_list('manager',
                                                                                            flat=True).distinct()
            manager_names = CustomUser.objects.filter(id__in=managers).values_list('username', flat=True)
            data["manager_names"] = ', '.join(manager_names) if manager_names else "No Managers assigned."

        elif user.role == "PM":
            projects_managed = Managers.objects.filter(manager=user).values_list('project', flat=True)
            data["project_members"] = Projectteams.objects.filter(project__in=projects_managed).values_list('member',
                                                                                                            flat=True)
            data["project_members"] = ", ".join(
                CustomUser.objects.filter(id__in=data["project_members"]).values_list('username', flat=True))

            if data["project_members"] == "":
                data["project_members"] = "No Members yet."

        if data["projects"] == "": data["projects"] = "No projects yet."

        return HttpResponse(json.dumps(data))

    else:
        return HttpResponse("Wrong Request..")


@login_required(login_url="/login/")
def editUser(request):
    if request.user.is_superuser and request.method == "POST":
        try:
            user = CustomUser.objects.get(id=request.POST['id'])
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.role = request.POST['role']
            if request.POST['password']!=user.password:
                user.set_password(request.POST['password'])
            user.save()

            errors = "User details updated Successfully..!"
        except Exception as e:
            errors = e.__str__()
        finally:
            users = list(CustomUser.objects.all())
            return render(request, "administrator/employees.html",
                          {"users": users, "errors": errors})

    else:
        return HttpResponse("Wrong Request..")


@login_required(login_url="/login/")
def editTask(request):
    if request.method == "POST":
        errors=""
        try:

            task = Tasks.objects.get(id=request.POST['taskid'])
            if task.user.id != request.user.id:
                raise Exception("Not Authorized")

            project = get_object_or_404(Projects, name=request.POST['project'])

            task.taskDescription = request.POST['taskDescription']
            task.accomplishments = request.POST['accomplishments']
            task.blockers = request.POST['blockers']
            task.project = project
            task.status = request.POST['status']
            task.save()

            errors = "Task details updated Successfully..!"
        except Exception as e:
            errors = e.__str__()
        finally:
            request.session["error"]=errors
            return redirect('/viewTasks/')

    else:
        return HttpResponse("Wrong Request..")


@login_required(login_url="/login")
def logoutUser(request):
    logout(request)
    return redirect("/login/")
