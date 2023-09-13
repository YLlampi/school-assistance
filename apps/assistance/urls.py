from django.urls import path

from . import views

app_name = 'assistance_app'

urlpatterns = [
    path('take_assistance/', views.TakeAssistanceView.as_view(), name='take_assistance'),
    path('register_assistance/', views.register_assistance, name='register_assistance'),
    path('report_assistance/', views.ReportAssistance.as_view(), name='report_assistance')
]