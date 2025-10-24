from django.shortcuts import render
from django.http import JsonResponse

def property_list(request):
    """매물 목록 페이지"""
    return render(request, 'property/list.html')

def property_detail(request, property_id):
    """매물 상세 페이지"""
    return render(request, 'property/detail.html', {'property_id': property_id})

def property_inquiry(request, property_id):
    """매물 문의하기"""
    return render(request, 'property/inquiry.html', {'property_id': property_id})
