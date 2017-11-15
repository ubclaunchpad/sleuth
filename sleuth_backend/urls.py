'''
Lists Sleuth's Django API endpoints
'''

from django.conf.urls import url
from .views import views

urlpatterns = [
    url(r'^search/', views.search, name='search'),
    url(r'^cores/', views.cores, name='cores'),
    url(r'^getdocument/', views.getdocument, name='getdocument'),
]