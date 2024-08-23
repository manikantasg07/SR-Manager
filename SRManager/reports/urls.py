from django.urls import path
from . import views
urlpatterns = [
    path("/",views.home,name="home"),
    path("login/",views.loginUser,name="login"),
    path("createTask/",views.createtask,name="createTask"),
    path("viewTasks/",views.viewTasks,name="viewTasks"),
    path("viewTasks/<int:taskId>/",views.viewSpeficTask,name="viewSpecificTasks"),
    path("viewMembersTasks/",views.memebersTasks,name="membersTasks"),
    path("viewMemberTasks/<int:userid>/",views.memberTasks,name="memberTasks"),
    path("executive/",views.executive,name="executive"),
    path("executiveMemberTasks/<int:userid>/",views.executiveMemberTasks,name="executiveMemberTasks"),
    path("users/",views.employees,name="user"),
    path("addUser/",views.addUser,name="addUser"),
    path("deleteUser/<int:userId>",views.deleteUser,name="deleteUser"),
    path("addProject/",views.addProject,name="addProject"),
    path("logout/",views.logoutUser,name="logout"),
    path("viewUser/<int:userId>/",views.viewSpeficUser,name="viewSpeficUser"),
    path("editUser/",views.editUser,name="editUser"),
    path("editTask/",views.editTask,name="editTask"),
]