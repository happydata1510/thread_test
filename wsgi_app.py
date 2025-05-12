#!/usr/bin/env python
"""WSGI 애플리케이션 래퍼 - Render 배포용"""

import os
import sys
import django

# 프로젝트 디렉토리 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'thread_generator'))

# 현재 경로 출력
print(f"Current directory: {os.getcwd()}")
print(f"BASE_DIR: {BASE_DIR}")
print(f"Python path: {sys.path}")

# 디렉토리 목록 표시
print("\nDirectory contents:")
for item in os.listdir('.'):
    print(f" - {item}")

if os.path.exists('thread_generator'):
    print("\nthread_generator contents:")
    for item in os.listdir('thread_generator'):
        print(f" - {item}")

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thread_generator.settings')

# 실제 WSGI 애플리케이션 생성
try:
    django.setup()
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("Successfully created WSGI application")
except Exception as e:
    print(f"Error setting up Django: {e}")
    
    # 대체 방법 시도
    if os.path.exists('thread_generator/thread_generator'):
        print("\nTrying alternative method...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thread_generator.thread_generator.settings')
        try:
            django.setup()
            from django.core.wsgi import get_wsgi_application
            application = get_wsgi_application()
            print("Successfully created WSGI application with alternative method")
        except Exception as e2:
            print(f"Alternative method also failed: {e2}")
            raise e2
    else:
        raise e 