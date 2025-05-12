# generator/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from .forms import CustomerForm, ThreadForm, ReviewForm, RevisionForm
from .models import Customer, GeneratedThread, Review, CopyLog, ThreadFeedback
from .utils import generate_content, revise_content
from .models import Thread
import uuid
from django.db import models
from django.conf import settings
import openai

from django.shortcuts import render, redirect
from .models import Customer, GeneratedThread
from .forms import CustomerForm, ThreadForm
from .utils import generate_content

def home(request):
    print("Method:", request.method)  # 디버깅: POST 요청이 오는지 확인
    
    # 통계 데이터 계산
    try:
        total_threads = GeneratedThread.objects.count()
        total_views = GeneratedThread.objects.aggregate(Sum('views'))['views__sum'] or 0
        avg_views = round(total_views / total_threads, 1) if total_threads > 0 else 0
    except Exception as e:
        print(f"Error calculating stats: {str(e)}")
        total_threads = 0
        total_views = 0
        avg_views = 0

    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        customer_form = CustomerForm(request.POST)
        
        print("Form validation:", thread_form.is_valid(), customer_form.is_valid())
        print("Form data:", request.POST)
        
        if thread_form.is_valid() and customer_form.is_valid():
            try:
                # 고객 정보 저장
                customer = customer_form.save()
                print(f"Customer saved: {customer.thread_id}")
                
                # 첫 번째 스타일의 쓰레드 생성
                thread1 = thread_form.save(commit=False)
                thread1.customer = customer
                content1 = generate_content(thread1.topic, thread1.style, thread1.requirements)
                thread1.content = content1
                thread1.views = 0
                thread1.save()
                print(f"Thread 1 saved: {thread1.topic}")
                
                # 두 번째 스타일의 쓰레드 생성
                second_style = 'story' if thread1.style != 'story' else 'informative'
                content2 = generate_content(thread1.topic, second_style, thread1.requirements)
                
                thread2 = GeneratedThread(
                    customer=customer,
                    topic=thread1.topic,
                    style=second_style,
                    requirements=thread1.requirements,
                    content=content2,
                    views=0
                )
                thread2.save()
                print(f"Thread 2 saved: {thread2.topic}")
                
                return render(request, 'ab_test_result.html', {
                    'thread1': thread1,
                    'thread2': thread2,
                    'success': True
                })
                
            except Exception as e:
                error_msg = f"컨텐츠 생성 중 오류가 발생했습니다: {str(e)}"
                print(error_msg)
                return render(request, 'home.html', {
                    'thread_form': thread_form,
                    'customer_form': customer_form,
                    'error': error_msg,
                    'total_threads': total_threads,
                    'total_views': total_views,
                    'avg_views': avg_views
                })
    else:
        thread_form = ThreadForm()
        customer_form = CustomerForm()
    
    return render(request, 'home.html', {
        'thread_form': thread_form,
        'customer_form': customer_form,
        'total_threads': total_threads,
        'total_views': total_views,
        'avg_views': avg_views
    })

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            # 임시로 첫 번째 고객을 연결 (실제로는 로그인된 사용자나 세션 정보를 사용해야 함)
            review.customer = Customer.objects.first()
            review.save()
            messages.success(request, '리뷰가 성공적으로 등록되었습니다.')
            return redirect('home')
    return redirect('home')

def thread_list(request):
    threads = GeneratedThread.objects.all().order_by('-created_at')[:10]
    return render(request, 'list.html', {'threads': threads})

def generate_ab_test(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        email = request.POST.get('email', '')
        ab_test_id = uuid.uuid4().hex[:8]  # A/B 테스트 그룹 식별자

        # 두 가지 다른 스타일로 컨텐츠 생성
        styles = request.POST.getlist('styles')  # 선택된 두 가지 스타일
        
        threads = []
        for i, style in enumerate(['informative', 'story']):  # 기본값으로 '정보형'과 '스토리형' 비교
            thread_id = f"thread_{ab_test_id}_{chr(65+i)}"  # A, B 버전
            content = generate_content(topic, style)
            
            thread = Thread.objects.create(
                thread_id=thread_id,
                topic=topic,
                style=style,
                content=content,
                email=email,
                ab_test_group=ab_test_id
            )
            threads.append(thread)

        return render(request, 'ab_test_result.html', {
            'threads': threads,
            'ab_test_id': ab_test_id
        })

    return render(request, 'home.html')

def select_version(request, thread_id):
    if request.method == 'POST':
        thread = Thread.objects.get(thread_id=thread_id)
        ab_test_group = thread.ab_test_group
        
        # 같은 테스트 그룹의 모든 쓰레드 선택 해제
        Thread.objects.filter(ab_test_group=ab_test_group).update(is_selected=False)
        
        # 선택된 버전만 선택 처리
        thread.is_selected = True
        thread.save()
        
        return redirect('view_thread', thread_id=thread_id)

def revise_thread(request, thread_id):
    thread = get_object_or_404(GeneratedThread, id=thread_id)
    
    if request.method == 'POST':
        form = RevisionForm(request.POST)
        if form.is_valid():
            # 수정 요청 데이터 저장
            thread.revision_prompt = form.cleaned_data['revision_prompt']
            thread.save()
            
            # 수정 적용 페이지로 리다이렉트
            return redirect('apply_revision', thread_id=thread.id)
    else:
        form = RevisionForm()
    
    return render(request, 'revise_thread.html', {
        'thread': thread,
        'form': form
    })

def apply_revision(request, thread_id):
    thread = get_object_or_404(GeneratedThread, id=thread_id)
    
    # 수정 프롬프트가 없으면 리다이렉트
    if not thread.revision_prompt:
        messages.error(request, '수정 요청사항이 없습니다.')
        return redirect('revise_thread', thread_id=thread.id)
    
    if request.method == 'POST':
        # 사용자가 수정 적용을 확인한 경우
        try:
            # 수정된 콘텐츠 저장
            thread.revised_content = request.POST.get('revised_content', '')
            thread.revised = True
            thread.save()
            messages.success(request, '콘텐츠가 성공적으로 수정되었습니다.')
            
            # 결과 페이지로 리다이렉트 (원래 A/B 테스트 결과 페이지와 비슷하지만 수정된 버전도 보여줌)
            return redirect('thread_list')
        except Exception as e:
            messages.error(request, f'콘텐츠 저장 중 오류가 발생했습니다: {str(e)}')
            return redirect('apply_revision', thread_id=thread.id)
    else:
        # API 호출하여 수정 콘텐츠 생성
        try:
            revised_content = revise_content(
                thread.content, 
                thread.revision_prompt,
                thread.topic,
                thread.style
            )
            
            return render(request, 'apply_revision.html', {
                'thread': thread,
                'revised_content': revised_content
            })
        except Exception as e:
            messages.error(request, f'콘텐츠 수정 중 오류가 발생했습니다: {str(e)}')
            return redirect('revise_thread', thread_id=thread.id)

def log_copy(request, thread_id):
    """
    스레드 복사 로그를 기록합니다.
    """
    thread = get_object_or_404(GeneratedThread, id=thread_id)
    
    # 복사 로그 생성
    copy_log = CopyLog(
        thread=thread,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    copy_log.save()
    
    # 복사 카운트 증가
    thread.copies += 1
    thread.save()
    
    return JsonResponse({'success': True, 'copies': thread.copies})

def thread_feedback(request, thread_id):
    """
    스레드에 대한 피드백(좋아요/싫어요)을 처리합니다.
    """
    thread = get_object_or_404(GeneratedThread, id=thread_id)
    feedback_type = request.POST.get('feedback_type')
    
    if feedback_type not in ['like', 'dislike']:
        return JsonResponse({'success': False, 'error': '유효하지 않은 피드백 유형입니다.'})
    
    ip_address = get_client_ip(request)
    
    # 이전 피드백이 있는지 확인
    existing_feedback = ThreadFeedback.objects.filter(thread=thread, ip_address=ip_address).first()
    
    # 피드백 처리
    if existing_feedback:
        # 이전과 같은 피드백이면 취소
        if existing_feedback.feedback_type == feedback_type:
            if feedback_type == 'like':
                thread.likes = max(0, thread.likes - 1)
            else:
                thread.dislikes = max(0, thread.dislikes - 1)
            existing_feedback.delete()
            is_canceled = True
        # 이전과 다른 피드백이면 업데이트
        else:
            if feedback_type == 'like':
                thread.likes += 1
                thread.dislikes = max(0, thread.dislikes - 1)
            else:
                thread.dislikes += 1
                thread.likes = max(0, thread.likes - 1)
            existing_feedback.feedback_type = feedback_type
            existing_feedback.save()
            is_canceled = False
    # 새 피드백 생성
    else:
        ThreadFeedback.objects.create(
            thread=thread,
            feedback_type=feedback_type,
            ip_address=ip_address
        )
        
        if feedback_type == 'like':
            thread.likes += 1
        else:
            thread.dislikes += 1
        is_canceled = False
    
    thread.save()
    
    return JsonResponse({
        'success': True, 
        'likes': thread.likes, 
        'dislikes': thread.dislikes,
        'is_canceled': is_canceled,
        'feedback_type': feedback_type
    })

def get_client_ip(request):
    """클라이언트 IP를 얻습니다."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip