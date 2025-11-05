from django.contrib import admin
from django import forms
from .models import PersonaType, AreaRecommendation, SurveyResult
import json

class ImageURLsWidget(forms.Textarea):
    """이미지 URL 목록을 여러 줄 텍스트로 입력받는 위젯"""
    def format_value(self, value):
        """JSON 리스트를 여러 줄 텍스트로 변환"""
        if value is None:
            return ''
        if isinstance(value, list):
            return '\n'.join(value)
        return str(value)
    
    def value_from_datadict(self, data, files, name):
        """여러 줄 텍스트를 JSON 리스트로 변환"""
        value = data.get(name, '')
        if not value:
            return []
        # 각 줄을 리스트 항목으로 변환 (빈 줄 제거)
        urls = [url.strip() for url in value.split('\n') if url.strip()]
        return urls

class AreaRecommendationAdminForm(forms.ModelForm):
    """지역 추천 Admin Form"""
    image_urls_display = forms.CharField(
        widget=ImageURLsWidget(attrs={'rows': 5, 'cols': 80}),
        required=False,
        help_text='각 줄에 하나씩 이미지 URL을 입력하세요. 예: https://example.com/image1.jpg',
        label='이미지 URL 목록 (한 줄에 하나씩)'
    )
    
    class Meta:
        model = AreaRecommendation
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # 기존 데이터를 여러 줄 텍스트로 변환
            self.fields['image_urls_display'].initial = '\n'.join(
                self.instance.image_urls or []
            )
        # 원래의 image_urls 필드는 숨김
        if 'image_urls' in self.fields:
            self.fields['image_urls'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # image_urls_display 값을 image_urls에 저장
        urls_text = self.cleaned_data.get('image_urls_display', '')
        if urls_text:
            urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
            instance.image_urls = urls
        else:
            instance.image_urls = []
        
        if commit:
            instance.save()
        return instance

@admin.register(PersonaType)
class PersonaTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color_code', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

@admin.register(AreaRecommendation)
class AreaRecommendationAdmin(admin.ModelAdmin):
    form = AreaRecommendationAdminForm
    list_display = ['area_name', 'district', 'matching_score', 'average_price', 'has_images']
    list_filter = ['district', 'matching_score']
    search_fields = ['area_name', 'district']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('area_name', 'district', 'matching_score', 'description')
        }),
        ('가격 및 점수', {
            'fields': ('average_price', 'transportation_score', 'education_score', 'lifestyle_score', 'investment_score')
        }),
        ('장단점', {
            'fields': ('advantages', 'disadvantages')
        }),
        ('이미지', {
            'fields': ('image_urls_display',),
            'description': '각 줄에 하나씩 이미지 URL을 입력하세요. 예: https://example.com/image1.jpg'
        }),
        ('시간 정보', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_images(self, obj):
        """이미지가 있는지 표시"""
        return bool(obj.image_urls and len(obj.image_urls) > 0)
    has_images.boolean = True
    has_images.short_description = '이미지 있음'

@admin.register(SurveyResult)
class SurveyResultAdmin(admin.ModelAdmin):
    list_display = ['survey', 'persona_type', 'matching_score', 'created_at']
    list_filter = ['persona_type', 'matching_score', 'created_at']
    search_fields = ['survey__user_name']
    readonly_fields = ['created_at']
