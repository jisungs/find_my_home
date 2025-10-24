from django.db import models
from django.utils import timezone

class Survey(models.Model):
    """설문 참여자 정보"""
    user_name = models.CharField(max_length=100, verbose_name="사용자 이름")
    email = models.EmailField(verbose_name="이메일")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="완료일")
    is_completed = models.BooleanField(default=False, verbose_name="완료 여부")
    
    class Meta:
        verbose_name = "설문"
        verbose_name_plural = "설문들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user_name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class SurveyQuestion(models.Model):
    """설문 문항 정보"""
    QUESTION_TYPES = [
        ('single', '단일 선택'),
        ('multiple', '다중 선택'),
        ('drag', '드래그 정렬'),
        ('slider', '슬라이더'),
        ('text', '텍스트 입력'),
    ]
    
    STEPS = [
        (1, 'STEP 1: 하드 필터'),
        (2, 'STEP 2: 감성 프로필'),
        (3, 'STEP 3: 현실 제약'),
    ]
    
    question_id = models.CharField(max_length=10, unique=True, verbose_name="문항 ID")
    question_text = models.TextField(verbose_name="문항 내용")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, verbose_name="문항 타입")
    options = models.JSONField(null=True, blank=True, verbose_name="선택 옵션")
    step = models.IntegerField(choices=STEPS, verbose_name="단계")
    order = models.IntegerField(verbose_name="순서")
    is_active = models.BooleanField(default=True, verbose_name="활성화")
    
    class Meta:
        verbose_name = "설문 문항"
        verbose_name_plural = "설문 문항들"
        ordering = ['step', 'order']
    
    def __str__(self):
        return f"{self.question_id}: {self.question_text[:50]}..."

class SurveyAnswer(models.Model):
    """설문 답변"""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="설문")
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, verbose_name="문항")
    answer = models.TextField(verbose_name="답변")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "설문 답변"
        verbose_name_plural = "설문 답변들"
        unique_together = ['survey', 'question']
    
    def __str__(self):
        return f"{self.survey.user_name} - {self.question.question_id}: {self.answer[:30]}..."
