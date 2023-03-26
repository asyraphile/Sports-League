from django.urls import path
from . import views

urlpatterns = [
    path('mainpage/', views.mainpage, name="Main Page"),
    path('team_list', views.team_list, name="Team List"),
    path('scoreboard', views.scoreboard, name="Scoreboard"),
    path('match_list/', views.match_list, name="Match List"),
    #auth
    path('login/', views.login, name="Login"),
    path('logout/', views.logout, name="Logout"),
    path('signup/', views.signup, name="Sign Up"),
    path('forgotpassword/', views.forgotpassword, name="Forgot Password"),
]