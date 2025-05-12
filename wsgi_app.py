#!/usr/bin/env python
"""WSGI 애플리케이션 래퍼 - Render 배포용"""

import os
import sys

# 프로젝트 디렉토리 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'thread_generator'))

# WSGI 애플리케이션 임포트
from thread_generator.thread_generator.wsgi import application

# 환경 정보 출력 (디버깅용)
if __name__ == '__main__':
    print(f"Python path: {sys.path}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Module search paths:")
    for path in sys.path:
        print(f"  - {path}") 