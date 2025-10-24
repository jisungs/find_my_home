from django.db import models
from django.utils import timezone

class Property(models.Model):
    """부산 매물 정보"""
    PROPERTY_TYPES = [
        ('단독주택', '단독주택'),
        ('타운하우스', '타운하우스'),
        ('빌라', '빌라'),
        ('연립주택', '연립주택'),
    ]
    
    PERSONA_MATCHES = [
        ('해안가_라이프스타일형', '해안가 라이프스타일형'),
        ('도심_라이프스타일형', '도심 라이프스타일형'),
        ('자연친화_크리에이티브형', '자연친화 크리에이티브형'),
        ('산업도시_자연친화형', '산업도시 자연친화형'),
        ('항만_라이프스타일형', '항만 라이프스타일형'),
        ('모던_미니멀형', '모던 미니멀형'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="제목")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='단독주택', verbose_name="매물 타입")
    location = models.CharField(max_length=100, verbose_name="상세 주소")
    district = models.CharField(max_length=50, verbose_name="구/군")
    price = models.IntegerField(verbose_name="가격 (원)")
    area = models.CharField(max_length=50, verbose_name="면적 정보")
    land_area = models.IntegerField(null=True, blank=True, verbose_name="대지면적 (평)")
    building_area = models.IntegerField(null=True, blank=True, verbose_name="건물면적 (평)")
    rooms = models.IntegerField(verbose_name="방 개수")
    bathrooms = models.IntegerField(verbose_name="화장실 개수")
    parking = models.IntegerField(verbose_name="주차 가능 대수")
    garden_area = models.IntegerField(null=True, blank=True, verbose_name="정원 면적 (평)")
    description = models.TextField(verbose_name="상세 설명")
    images = models.JSONField(default=list, verbose_name="이미지 URL 목록")
    persona_match = models.CharField(max_length=50, choices=PERSONA_MATCHES, verbose_name="페르소나 매칭")
    
    # 점수 시스템
    transportation_score = models.IntegerField(default=0, verbose_name="교통 점수")
    education_score = models.IntegerField(default=0, verbose_name="교육 점수")
    lifestyle_score = models.IntegerField(default=0, verbose_name="생활 점수")
    investment_score = models.IntegerField(default=0, verbose_name="투자 점수")
    
    # 상태 관리
    is_active = models.BooleanField(default=True, verbose_name="활성화")
    is_featured = models.BooleanField(default=False, verbose_name="추천 매물")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    
    class Meta:
        verbose_name = "매물"
        verbose_name_plural = "매물들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.location} ({self.price:,}원)"
    
    def get_main_image(self):
        """메인 이미지 반환"""
        if self.images and len(self.images) > 0:
            return self.images[0]
        return None
    
    def get_price_display(self):
        """가격 표시 형식"""
        if self.price >= 100000000:  # 1억 이상
            return f"{self.price // 100000000}억 {self.price % 100000000 // 10000}만원"
        elif self.price >= 10000:  # 1만 이상
            return f"{self.price // 10000}만원"
        else:
            return f"{self.price:,}원"

class PropertyImage(models.Model):
    """매물 이미지"""
    IMAGE_TYPES = [
        ('main', '메인 이미지'),
        ('interior', '내부 이미지'),
        ('exterior', '외부 이미지'),
        ('garden', '정원 이미지'),
        ('surrounding', '주변 환경'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="매물")
    image_url = models.URLField(verbose_name="이미지 URL")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='main', verbose_name="이미지 타입")
    order = models.IntegerField(default=0, verbose_name="순서")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "매물 이미지"
        verbose_name_plural = "매물 이미지들"
        ordering = ['property', 'order']
    
    def __str__(self):
        return f"{self.property.title} - {self.image_type}"

class PropertyInquiry(models.Model):
    """매물 문의"""
    INQUIRY_TYPES = [
        ('viewing', '방문 상담'),
        ('price', '가격 문의'),
        ('loan', '대출 문의'),
        ('other', '기타'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, verbose_name="매물")
    name = models.CharField(max_length=100, verbose_name="이름")
    phone = models.CharField(max_length=20, verbose_name="연락처")
    email = models.EmailField(verbose_name="이메일")
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='viewing', verbose_name="문의 유형")
    message = models.TextField(verbose_name="문의 내용")
    is_contacted = models.BooleanField(default=False, verbose_name="연락 완료")
    contacted_at = models.DateTimeField(null=True, blank=True, verbose_name="연락 완료일")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")
    
    class Meta:
        verbose_name = "매물 문의"
        verbose_name_plural = "매물 문의들"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.property.title} ({self.inquiry_type})"
