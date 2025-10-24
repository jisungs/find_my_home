from django.shortcuts import render
from django.http import JsonResponse

def survey_start(request):
    """설문 시작 페이지"""
    return render(request, 'survey/start.html')

def survey_question(request, question_id):
    """개별 문항 페이지"""
    return render(request, 'survey/question.html', {'question_id': question_id})

def survey_complete(request, survey_id):
    """설문 완료 처리"""
    return render(request, 'survey/complete.html', {'survey_id': survey_id})
