from django.contrib import admin
from .models import Property, PropertyImage, PropertyInquiry

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'district', 'price', 'persona_match', 'is_active', 'is_featured']
    list_filter = ['district', 'property_type', 'persona_match', 'is_active', 'is_featured']
    search_fields = ['title', 'location', 'description']
    readonly_fields = ['created_at', 'updated_at']
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

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'image_type', 'order', 'created_at']
    list_filter = ['image_type', 'created_at']
    search_fields = ['property__title']
    readonly_fields = ['created_at']

@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'property', 'inquiry_type', 'is_contacted', 'created_at']
    list_filter = ['inquiry_type', 'is_contacted', 'created_at']
    search_fields = ['name', 'phone', 'email', 'property__title']
    readonly_fields = ['created_at']
