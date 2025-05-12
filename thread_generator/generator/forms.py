# generator/forms.py
from django import forms
from .models import Review, Thread
import uuid
from django import forms
from .models import Customer, GeneratedThread


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['thread_id']
        widgets = {
            'thread_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '스레드 ID를 입력하세요'
            })
        }

    def clean_thread_id(self):
        thread_id = self.cleaned_data.get('thread_id')
        if not thread_id:
            raise forms.ValidationError("스레드 ID를 입력해주세요.")
        return thread_id

# forms.py의 ThreadForm 클래스 수정
class ThreadForm(forms.ModelForm):
    STYLE_CHOICES = [
        ('informative', '💡 정보형'),
        ('funny', '😆 유머형'),
        ('motivational', '🔥 동기부여형'),
        ('story', '📖 스토리형'),
    ]
    
    style = forms.ChoiceField(
        choices=STYLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = GeneratedThread
        fields = ['topic', 'style', 'requirements']
        widgets = {
            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '주제를 입력하세요'
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '추가적인 세부 요건을 입력하세요 (선택사항)',
                'rows': 3
            })
        }

    def clean_topic(self):
        topic = self.cleaned_data.get('topic')
        if not topic:
            raise forms.ValidationError("주제를 입력해주세요.")
        return topic

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class RevisionForm(forms.Form):
    revision_prompt = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '이 글을 어떻게 수정하면 좋을지 자세히 알려주세요',
            'rows': 4
        }),
        label='수정 요청사항',
        help_text='예: "첫 문장이 더 강렬하게 시작했으면 좋겠어요" 또는 "실제 사례를 추가해주세요"'
    )