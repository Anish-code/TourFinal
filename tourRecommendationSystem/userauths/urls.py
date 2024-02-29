from django.urls import path

from userauths import views

app_name='userauths'


urlpatterns = [
    path("sign-in/",views.login_view, name="sign-in"),
    path("sign-out/", views.logout_view, name="sign-out"),
    path('login/', views.login_view, name='login'),
]