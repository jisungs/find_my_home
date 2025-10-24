from django.contrib import admin
from .models import PersonaType, AreaRecommendation, SurveyResult

@admin.register(PersonaType)
class PersonaTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color_code', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(AreaRecommendation)
class AreaRecommendationAdmin(admin.ModelAdmin):
    list_display = ['area_name', 'district', 'matching_score', 'average_price']
    list_filter = ['district', 'matching_score']
    search_fields = ['area_name', 'district']
    readonly_fields = ['created_at']

@admin.register(SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    list_display = ['survey', 'persona_type', 'matching_score', 'created_at']
    list_filter = ['persona_type', 'matching_score', 'created_at']
    search_fields = ['survey__user_name']
    readonly_fields = ['created_at']
