from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name="home"),
    path('login/',views.login_user,name="login"),
    path('questions',views.show_questions,name="questions"),
    path('create',views.create,name="create"),
    path('logout/',views.logout_user,name="logout"),
    path('user_response',views.user_response,name="user_response"),
    path('my_responses',views.my_responses,name='my_responses'),
    path('exit_game',views.exit_game,name="exit_game"),
]
