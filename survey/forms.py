from django import forms
from .models import Survey, SurveyAnswer, SurveyQuestion

class SurveyStartForm(forms.ModelForm):
    """설문 시작 폼"""
    class Meta:
        model = Survey
        fields = ['user_name', 'email']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름을 입력해주세요'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일을 입력해주세요'
            })
        }

class SurveyAnswerForm(forms.Form):
    """설문 답변 폼"""
    answer = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if question.question_type == 'single':
            choices = [(opt, opt) for opt in question.options]
            self.fields['answer'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                label=question.question_text
            )
        elif question.question_type == 'multiple':
            choices = [(opt, opt) for opt in question.options]
            self.fields['answer'] = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                label=question.question_text
            )
        elif question.question_type == 'drag':
            # 드래그 정렬은 JavaScript로 처리
            self.fields['answer'] = forms.CharField(
                widget=forms.HiddenInput(),
                label=question.question_text
            )
        elif question.question_type == 'slider':
            # 슬라이더는 JavaScript로 처리
            self.fields['answer'] = forms.IntegerField(
                widget=forms.HiddenInput(),
                label=question.question_text
            )
        elif question.question_type == 'text':
            self.fields['answer'] = forms.CharField(
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': '답변을 입력해주세요'
                }),
                label=question.question_text
            )
