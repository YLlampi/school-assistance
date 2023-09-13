from django.urls import path
from . import views

from .views_PDF import print_qr_pdf

app_name = 'student_app'


urlpatterns = [
    path('generate_qr/', views.GenerateQrView.as_view(), name='generate_qr'),

    path('import_xlsx/', views.import_xlsx, name='import_xlsx'),

    path('print_qr_pdf/<int:id_student>/<int:id_classroom>/', print_qr_pdf, name='print_qr_pdf'),

]
