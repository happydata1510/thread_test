# 쓰레드 컨텐츠 생성기

Django 기반의 웹 애플리케이션으로, 사용자가 주제와 스타일을 입력하면 ChatGPT API를 활용하여 쓰레드용 콘텐츠를 자동으로 생성합니다.

## 주요 기능

1. 사용자가 주제, 스타일, 추가 요건을 입력하면 OpenAI API를 통해 콘텐츠 생성
2. A/B 테스트: 동일한 주제로 두 가지 다른 스타일의 콘텐츠 생성 및 비교
3. 생성된 콘텐츠를 수정할 수 있는 기능 (revision 기능)
4. 콘텐츠 생성 시 글자 수 제한(450자 내외) 및 포맷팅 최적화
5. 강력한 훅(Hook) 문장으로 시작하는 콘텐츠 구조
6. 복사 버튼 클릭 시 데이터베이스에 로그 저장 기능
7. 좋아요/싫어요 피드백 기능 및 데이터베이스 저장

## 설치 및 실행 방법

### 로컬 개발 환경 설정

1. 저장소 클론
   ```
   git clone [repository-url]
   cd thread_generator
   ```

2. 가상 환경 설정
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. 의존성 설치
   ```
   pip install -r requirements.txt
   ```

4. 환경 변수 설정
   `.env` 파일을 생성하고 다음 값을 설정:
   ```
   OPENAI_API_KEY=your_openai_api_key
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ```

5. 데이터베이스 마이그레이션
   ```
   python manage.py migrate
   ```

6. 개발 서버 실행
   ```
   python manage.py runserver
   ```

### Render로 배포

1. GitHub 저장소에 프로젝트 푸시
2. Render 대시보드(dashboard.render.com)에서 새 웹 서비스 생성
3. GitHub 저장소 연결
4. `render.yaml` 설정을 사용하여 Blueprint로 배포 또는 수동 설정
5. 환경 변수에 `OPENAI_API_KEY` 설정

## 콘텐츠 생성 프롬프트 규칙

1. 첫 문장은 반드시 강력한 훅으로 시작하고 줄바꿈
2. 2-3문장마다 자연스러운 줄바꿈으로 가독성 향상
3. 짧고 간결한 문장 사용 (15자 내외)
4. 부드럽고 친근한 말투로 작성
5. 독자와 소통하는 느낌의 글 작성
6. 명확한 콜투액션으로 마무리 