from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from .models import Survey, SurveyQuestion, SurveyAnswer
from .forms import SurveyStartForm, SurveyAnswerForm
import json

def survey_start(request):
    """설문 시작 페이지"""
    if request.method == 'POST':
        form = SurveyStartForm(request.POST)
        if form.is_valid():
            survey = form.save()
            return redirect('survey:survey_question', question_id='Q1', survey_id=survey.id)
    else:
        form = SurveyStartForm()
    
    return render(request, 'survey/start.html', {'form': form})

def survey_question(request, question_id, survey_id):
    """개별 문항 페이지"""
    survey = get_object_or_404(Survey, id=survey_id)
    question = get_object_or_404(SurveyQuestion, question_id=question_id, is_active=True)
    
    # 이미 답변한 문항인지 확인
    existing_answer = SurveyAnswer.objects.filter(survey=survey, question=question).first()
    
    if request.method == 'POST':
        form = SurveyAnswerForm(question, request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['answer']
            
            # 다중 선택의 경우 JSON으로 저장
            if question.question_type == 'multiple':
                answer_text = json.dumps(answer_text)
            
            # 답변 저장 또는 업데이트
            if existing_answer:
                existing_answer.answer = answer_text
                existing_answer.save()
            else:
                SurveyAnswer.objects.create(
                    survey=survey,
                    question=question,
                    answer=answer_text
                )
            
            # 다음 문항으로 이동
            next_question = get_next_question(question)
            if next_question:
                return redirect('survey:survey_question', 
                              question_id=next_question.question_id, 
                              survey_id=survey_id)
            else:
                # 설문 완료
                survey.is_completed = True
                survey.save()
                return redirect('survey:survey_complete', survey_id=survey_id)
    else:
        # 기존 답변이 있으면 폼에 표시
        initial_data = {}
        if existing_answer:
            if question.question_type == 'multiple':
                try:
                    initial_data['answer'] = json.loads(existing_answer.answer)
                except:
                    initial_data['answer'] = existing_answer.answer
            else:
                initial_data['answer'] = existing_answer.answer
        
        form = SurveyAnswerForm(question, initial=initial_data)
    
    # 진행률 계산
    total_questions = SurveyQuestion.objects.filter(is_active=True).count()
    completed_questions = SurveyAnswer.objects.filter(survey=survey).count()
    progress = int((completed_questions / total_questions) * 100)
    
    context = {
        'form': form,
        'question': question,
        'survey': survey,
        'progress': progress,
        'step': question.step,
        'step_name': question.get_step_display(),
    }
    
    return render(request, 'survey/question.html', context)

def survey_complete(request, survey_id):
    """설문 완료 처리"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    # 설문 결과 생성 (임시로 기본값 설정)
    from results.models import PersonaType, SurveyResult
    
    # 기본 페르소나 선택 (나중에 알고리즘으로 대체)
    default_persona = PersonaType.objects.first()
    
    if not SurveyResult.objects.filter(survey=survey).exists():
        SurveyResult.objects.create(
            survey=survey,
            persona_type=default_persona,
            matching_score=85,
            recommended_areas=[],
            recommended_properties=[]
        )
    
    return render(request, 'survey/complete.html', {'survey': survey})

def survey_progress(request, survey_id):
    """설문 진행률 API"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    total_questions = SurveyQuestion.objects.filter(is_active=True).count()
    completed_questions = SurveyAnswer.objects.filter(survey=survey).count()
    progress = int((completed_questions / total_questions) * 100)
    
    return JsonResponse({
        'progress': progress,
        'completed': completed_questions,
        'total': total_questions
    })

def get_next_question(current_question):
    """다음 문항 반환"""
    next_question = SurveyQuestion.objects.filter(
        is_active=True,
        step=current_question.step,
        order__gt=current_question.order
    ).first()
    
    if not next_question:
        # 같은 단계에 다음 문항이 없으면 다음 단계의 첫 번째 문항
        next_question = SurveyQuestion.objects.filter(
            is_active=True,
            step__gt=current_question.step
        ).order_by('step', 'order').first()
    
    return next_question
