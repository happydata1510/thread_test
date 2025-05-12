"""Gunicorn 설정 파일"""

import os
import sys
import multiprocessing

# 프로젝트 경로 추가
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'thread_generator'))

# Gunicorn 설정
bind = "0.0.0.0:10000"  # Render가 사용하는 기본 포트
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
keepalive = 5

# 로그 설정
errorlog = "-"  # stderr로 로그 출력
accesslog = "-"  # stdout으로 로그 출력
loglevel = "info"

# 애플리케이션 설정
wsgi_app = "wsgi_app:application"

# 시작 전 초기화
def on_starting(server):
    print(f"Starting Gunicorn with Python path: {sys.path}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Available modules: {[m for m in sys.modules.keys()][:20]}")  # 처음 20개만 출력 