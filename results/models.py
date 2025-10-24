from django.db import models
from django.utils import timezone

class PersonaType(models.Model):
    """페르소나 타입 정의"""
    PERSONA_CHOICES = [
        ('해안가_라이프스타일형', '해안가 라이프스타일형'),
        ('도심_라이프스타일형', '도심 라이프스타일형'),
        ('자연친화_크리에이티브형', '자연친화 크리에이티브형'),
        ('산업도시_자연친화형', '산업도시 자연친화형'),
        ('항만_라이프스타일형', '항만 라이프스타일형'),
        ('모던_미니멀형', '모던 미니멀형'),
    ]
    
    name = models.CharField(max_length=50, choices=PERSONA_CHOICES, unique=True, verbose_name="페르소나명")
    description = models.TextField(verbose_name="설명")
    color_code = models.CharField(max_length=7, default="#4A90E2", verbose_name="색상 코드")
    icon = models.CharField(max_length=20, default="🏠", verbose_name="아이콘")
    characteristics = models.JSONField(default=dict, verbose_name="특성")
    recommended_areas = models.JSONField(default=list, verbose_name="추천 지역")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "페르소나 타입"
        verbose_name_plural = "페르소나 타입들"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AreaRecommendation(models.Model):
    """지역 추천 정보"""
    area_name = models.CharField(max_length=100, verbose_name="지역명")
    district = models.CharField(max_length=50, verbose_name="구/군")
    matching_score = models.IntegerField(verbose_name="매칭 점수")
    description = models.TextField(verbose_name="설명")
    advantages = models.JSONField(default=list, verbose_name="장점")
    disadvantages = models.JSONField(default=list, verbose_name="단점")
    average_price = models.IntegerField(verbose_name="평균 가격")
    transportation_score = models.IntegerField(default=0, verbose_name="교통 점수")
    education_score = models.IntegerField(default=0, verbose_name="교육 점수")
    lifestyle_score = models.IntegerField(default=0, verbose_name="생활 점수")
    investment_score = models.IntegerField(default=0, verbose_name="투자 점수")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "지역 추천"
        verbose_name_plural = "지역 추천들"
        ordering = ['-matching_score']
    
    def __str__(self):
        return f"{self.area_name} ({self.district}) - {self.matching_score}점"

class SurveyResult(models.Model):
    """설문 결과"""
    survey = models.OneToOneField('survey.Survey', on_delete=models.CASCADE, verbose_name="설문")
    persona_type = models.ForeignKey(PersonaType, on_delete=models.CASCADE, verbose_name="페르소나 타입")
    matching_score = models.IntegerField(verbose_name="매칭 점수")
    recommended_areas = models.JSONField(default=list, verbose_name="추천 지역")
    recommended_properties = models.JSONField(default=list, verbose_name="추천 매물")
    detailed_analysis = models.JSONField(default=dict, verbose_name="상세 분석")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "설문 결과"
        verbose_name_plural = "설문 결과들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.survey.user_name} - {self.persona_type.name} ({self.matching_score}점)"
    
    def get_top_recommended_areas(self, limit=3):
        """상위 추천 지역 반환"""
        return self.recommended_areas[:limit]
    
    def get_top_recommended_properties(self, limit=3):
        """상위 추천 매물 반환"""
        return self.recommended_properties[:limit]
    
    def get_matching_reasons(self):
        """매칭 이유 반환"""
        return self.detailed_analysis.get('matching_reasons', [])
    
    def get_persona_description(self):
        """페르소나 설명 반환"""
        return self.detailed_analysis.get('persona_description', {})
    
    def get_radar_chart_data(self):
        """레이더 차트 데이터 반환"""
        return self.detailed_analysis.get('radar_chart_data', {})
