from django.urls import include, path
from core.views import index, services,tour_detail_view, getrecommendation, explore, gallery, blogs, contact, userdashboard, button_clicked, get_recommendations, tour_details

app_name="core"

urlpatterns = [
    path('', index, name="index"),
    path('services/',services, name="services"),
    path('getrecommendation/',getrecommendation,name="getrecommendation"),
        path('tourdescription/<int:tid>/',tour_detail_view, name="tourdescription"),

    path('explore/',explore,name="explore"),
    path('gallery/',gallery,name="gallery"),
    path('blogs/', blogs, name="blogs"),
    path('contact/',contact, name="contact"),
    path('button/',button_clicked, name="button"),
    path('userdashboard', userdashboard, name="userdashboard" ),
    path('get_recommendation/<int:item_id>/', get_recommendations, name="get_recommendation"),
    path('tour-detail/<int:item_id>/', tour_details, name="tour-detail"),


]