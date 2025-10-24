from django.contrib import admin
from .models import Survey, SurveyQuestion, SurveyAnswer

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'email', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user_name', 'email']
    readonly_fields = ['created_at']

@admin.register(SurveyQuestion)
class SurveyQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'question_text', 'question_type', 'step', 'order', 'is_active']
    list_filter = ['step', 'question_type', 'is_active']
    search_fields = ['question_text']
    ordering = ['step', 'order']

@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ['survey', 'question', 'answer', 'created_at']
    list_filter = ['question__step', 'created_at']
    search_fields = ['survey__user_name', 'answer']
    readonly_fields = ['created_at']
