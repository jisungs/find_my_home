from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Property

def property_list(request):
    """매물 목록 페이지"""
    # 필터링 옵션
    persona_match = request.GET.get('persona', '')
    district = request.GET.get('district', '')
    search_query = request.GET.get('search', '')
    
    # 기본 쿼리셋
    properties = Property.objects.filter(is_active=True)
    
    # 필터링 적용
    if persona_match:
        properties = properties.filter(persona_match=persona_match)
    
    if district:
        properties = properties.filter(district=district)
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # 페르소나 타입 목록 (필터용)
    persona_types = Property.PERSONA_MATCHES
    
    # 구/군 목록 (필터용)
    districts = Property.objects.filter(is_active=True).values_list('district', flat=True).distinct()
    
    context = {
        'properties': properties,
        'persona_types': persona_types,
        'districts': districts,
        'selected_persona': persona_match,
        'selected_district': district,
        'search_query': search_query,
    }
    
    return render(request, 'property/list.html', context)

def property_detail(request, property_id):
    """매물 상세 페이지"""
    property_obj = get_object_or_404(Property, id=property_id, is_active=True)
    
    # 같은 페르소나 매칭 매물 추천 (최대 3개)
    recommended_properties = Property.objects.filter(
        persona_match=property_obj.persona_match,
        is_active=True
    ).exclude(id=property_id)[:3]
    
    # description에서 구조화된 정보 추출
    description_text = property_obj.description
    transportation_info = ""
    education_info = ""
    surrounding_info = ""
    
    # description을 줄바꿈으로 분리하여 각 섹션 추출
    lines = description_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('[교통]'):
            current_section = 'transportation'
            continue
        elif line.startswith('[학군]'):
            current_section = 'education'
            continue
        elif line.startswith('[기타 주변환경]'):
            current_section = 'surrounding'
            continue
        elif line.startswith('['):
            current_section = None
            continue
        
        if current_section == 'transportation' and line:
            transportation_info += line + "\n"
        elif current_section == 'education' and line:
            education_info += line + "\n"
        elif current_section == 'surrounding' and line:
            surrounding_info += line + "\n"
    
    context = {
        'property': property_obj,
        'recommended_properties': recommended_properties,
        'transportation_info': transportation_info.strip(),
        'education_info': education_info.strip(),
        'surrounding_info': surrounding_info.strip(),
    }
    
    return render(request, 'property/detail.html', context)

def property_inquiry(request, property_id):
    """매물 문의하기"""
    property_obj = get_object_or_404(Property, id=property_id, is_active=True)
    
    if request.method == 'POST':
        # TODO: 문의 폼 처리 로직 추가
        pass
    
    return render(request, 'property/inquiry.html', {'property': property_obj})
