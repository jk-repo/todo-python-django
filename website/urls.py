from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='login_url'),
    path('signup', views.signup, name='signup_url'),
    path('signout', views.signout, name='signout_url'),
    path('dashboard', views.dashboard, name='dashboard_url'),
    path('profile', views.profile, name='profile_url'),
    path('updatePassword', views.updatePassword, name='updatePassword_url'),
    path('addTodo', views.addTodo, name='addTodo_url'),
    path('updateTodo', views.updateTodo, name='updateTodo_url'),
    path('deleteTodo', views.deleteTodo, name='deleteTodo_url'),
]
