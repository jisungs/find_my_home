from django.urls import path
from . import views

app_name = 'survey'

urlpatterns = [
    path('', views.survey_start, name='survey_start'),
    path('question/<str:question_id>/', views.survey_question, name='survey_question'),
    path('complete/<int:survey_id>/', views.survey_complete, name='survey_complete'),
]
