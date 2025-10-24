from django.shortcuts import render
from django.http import JsonResponse

def show_result(request, survey_id):
    """결과 페이지 표시"""
    return render(request, 'results/result.html', {'survey_id': survey_id})

def share_result(request, survey_id):
    """결과 공유 기능"""
    return render(request, 'results/share.html', {'survey_id': survey_id})
