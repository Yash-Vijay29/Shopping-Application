from django.urls import path
from . import views
app_name = 'ocrapp'

urlpatterns = [
    path('', views.homepage, name='home'),
    path('manual_search', views.manualsearch, name='home'),
    path('details/<path:product_url>/',views.details,name='details'),
]
