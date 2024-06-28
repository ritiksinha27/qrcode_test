from django.urls import path
from .views import *

urlpatterns = [
    path('generate_qr/', generate_qr, name='generate_qr'),
      path('scan/image/', scan_qr_image, name='scan_qr_image'),
     path('live_camera/', live_camera, name='live_camera'),
       path('check_qr_data/', check_qr_data, name='check_qr_data'),
    path('process_qr_data/', process_qr_data, name='process_qr_data'),
    path('scan/live/', scan_qr_live, name='scan_qr_live'),
]