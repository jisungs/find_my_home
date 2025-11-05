from django.contrib import admin
from .models import Property, PropertyImage, PropertyInquiry


class PropertyImageInline(admin.TabularInline):
    """매물 이미지 인라인"""
    model = PropertyImage
    extra = 1
    fields = ('image_url', 'image_type', 'order', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('order', 'created_at')
    verbose_name = "매물 이미지"
    verbose_name_plural = "매물 이미지들"


class PropertyInquiryInline(admin.TabularInline):
    """매물 문의 인라인"""
    model = PropertyInquiry
    extra = 0
    fields = ('name', 'phone', 'email', 'inquiry_type', 'message', 'is_contacted', 'contacted_at', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    verbose_name = "매물 문의"
    verbose_name_plural = "매물 문의들"
    can_delete = False  # 문의는 삭제하지 못하도록 (옵션, 필요시 변경 가능)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'district', 'price', 'persona_match', 'is_active', 'is_featured']
    list_filter = ['district', 'property_type', 'persona_match', 'is_active', 'is_featured']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PropertyImageInline, PropertyInquiryInline]
    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'property_type', 'location', 'district', 'price', 'area')
        }),
        ('상세 정보', {
            'fields': ('land_area', 'building_area', 'rooms', 'bathrooms', 'parking', 'garden_area')
        }),
        ('설명 및 이미지', {
            'fields': ('description', 'images')
        }),
        ('매칭 정보', {
            'fields': ('persona_match', 'transportation_score', 'education_score', 'lifestyle_score', 'investment_score')
        }),
        ('상태 관리', {
            'fields': ('is_active', 'is_featured')
        }),
        ('시간 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
