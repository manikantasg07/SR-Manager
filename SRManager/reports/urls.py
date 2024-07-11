from django.urls import path
from . import views
urlpatterns = [
    path("login/",views.loginUser,name="login"),
    path("createTask/",views.createtask,name="createTask"),
    path("viewTasks/",views.viewTasks,name="viewTasks"),
    path("viewMembersTasks/",views.memebersTasks,name="membersTasks"),
    path("viewMemberTasks/<int:userid>/",views.memberTasks,name="memberTasks"),
    path("logout/",views.logoutUser,name="logout")
]