from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('registration/', views.registration, name='registration'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
]
