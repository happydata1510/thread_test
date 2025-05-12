#!/usr/bin/env python
"""WSGI 애플리케이션 래퍼 - Render 배포용"""

import os
import sys

# 프로젝트 디렉토리 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'thread_generator'))

# 현재 경로 출력
print(f"Current directory: {os.getcwd()}")
print(f"BASE_DIR: {BASE_DIR}")
print(f"Python path: {sys.path}")

# 실제 Django WSGI 구현 - 이미 존재하는 모듈에서 직접 임포트
try:
    from thread_generator.thread_generator.wsgi import application
    print("Successfully imported application from thread_generator.thread_generator.wsgi")
except ImportError as e:
    print(f"Import error: {e}")
    # 대체 방법
    import django
    from django.core.wsgi import get_wsgi_application
    
    # Django 설정
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thread_generator.thread_generator.settings')
    django.setup()
    
    # WSGI 애플리케이션 가져오기
    application = get_wsgi_application()
    print("Using fallback method to get WSGI application")

# 디버깅을 위해 가능한 모든 디렉토리 내용 출력
print("\nListing important directories:")
print("\nContents of current directory:")
for item in os.listdir('.'):
    print(f" - {item}")

if os.path.exists('thread_generator'):
    print("\nContents of thread_generator directory:")
    for item in os.listdir('thread_generator'):
        print(f" - {item}")
        
    if os.path.exists('thread_generator/thread_generator'):
        print("\nContents of thread_generator/thread_generator directory:")
        for item in os.listdir('thread_generator/thread_generator'):
            print(f" - {item}") 