from django.urls import include, path
from core.views import index, services, getrecommendation, explore, gallery, blogs, contact, userdashboard

app_name="core"

urlpatterns = [
    path('', index, name="index"),
    path('services/',services, name="services"),
    path('getrecommendation/',getrecommendation,name="getrecommendation"),
    path('explore/',explore,name="explore"),
    path('gallery/',gallery,name="gallery"),
    path('blogs/', blogs, name="blogs"),
    path('contact/',contact, name="contact"),
    path('userdashboard', userdashboard, name="userdashboard" ),
]