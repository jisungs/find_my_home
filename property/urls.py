from django.urls import path
from . import views

app_name = 'property'

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('detail/<int:property_id>/', views.property_detail, name='property_detail'),
    path('inquiry/<int:property_id>/', views.property_inquiry, name='property_inquiry'),
]
