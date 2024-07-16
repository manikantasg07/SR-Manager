from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.loginUser,name="login"),
    path("createTask/",views.createtask,name="createTask"),
    path("viewTasks/",views.viewTasks,name="viewTasks"),
    path("viewTasks/<int:taskId>/",views.viewSpeficTask,name="viewSpecificTasks"),
    path("viewMembersTasks/",views.memebersTasks,name="membersTasks"),
    path("viewMemberTasks/<int:userid>/",views.memberTasks,name="memberTasks"),
    path("executive/",views.executive,name="executive"),
    path("executiveMemberTasks/<int:userid>/",views.executiveMemberTasks,name="executiveMemberTasks"),
    path("addUser/",views.addUser,name="addUser"),
    path("addProject/",views.addProject,name="addUser"),
    path("logout/",views.logoutUser,name="logout")
]