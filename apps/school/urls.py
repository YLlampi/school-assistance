from django.urls import path
from . import views

app_name = 'school_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

]
