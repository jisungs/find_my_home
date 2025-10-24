from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('result/<int:survey_id>/', views.show_result, name='show_result'),
    path('share/<int:survey_id>/', views.share_result, name='share_result'),
]
