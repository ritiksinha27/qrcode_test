from django.urls import path,include
from .views import *
urlpatterns = [
    path('',KYCViews.as_view(),name='kyc'),
]