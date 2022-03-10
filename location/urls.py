from django.urls import path
from .views import home
app_name = 'location'

urlpatterns =[

    path('map/', home, name='map'),

 ]
