# generator/utils.py
import openai
from django.conf import settings
from openai import OpenAI

def generate_content(topic, style, requirements=None):
    print(f"Generating content for topic: {topic}, style: {style}, requirements: {requirements}")
    
    style_prompts = {
        'informative': "당신은 400-450자(공백 포함) 내외로 유익한 정보와 통찰을 제공하는 스레드 작성 전문가입니다.",
        'funny': "당신은 400-450자(공백 포함) 내외로 사람들이 웃으며 공감하는 유머러스한 스레드 작성 전문가입니다.",
        'motivational': "당신은 400-450자(공백 포함) 내외로 사람들에게 동기부여를 주는 스레드 작성 전문가입니다.",
        'story': "당신은 400-450자(공백 포함) 내외로 사람들이 몰입하는 이야기 스레드 작성 전문가입니다."
    }

    hook_examples = """
    강력한 훅 문장 예시 (첫 문장에 반드시 사용하세요):
    질문형: "왜 대부분의 사람들이 {topic}을 잘못 이해할까요?"
    공감형: "{topic}에 대해 아무도 알려주지 않는 진짜 팁들"
    충격형: "{topic}을 모르면 앞으로 경쟁에서 살아남을 수 없습니다"
    리스트형: "단 3개월 만에 {topic} 마스터한 5가지 방법"
    비밀공개형: "{topic}에 대한 업계의 숨겨진 비밀"
    호기심유발형: "{topic}에 관한 가장 놀라운 사실을 아시나요?"
    관찰형: "요즘 주변을 보면 {topic}에 대한 오해가 너무 많아요"
    공통의 적형: "{topic}때문에 우리 모두 힘들었던 경험 있으시죠?"
    직접경험형: "제가 {topic}을 경험하면서 깨달은 중요한 한 가지"
    """

    cta_examples = """
    콜투액션(CTA) 예시:
    "여러분은 어떻게 생각하시나요?"
    "당신의 {topic} 경험을 댓글로 알려주세요"
    "이 글이 도움되었다면 저장해두세요"
    "공감한다면 공유해주세요"
    "더 많은 팁이 필요하다면 팔로우하세요"
    """

    # 추가 요건이 있는 경우 프롬프트에 포함
    additional_requirements = ""
    if requirements:
        additional_requirements = f"""
        추가 요건:
        {requirements}
        
        위의 추가 요건을 반드시 콘텐츠에 반영하세요.
        """

    prompt = f"""
    주제: {topic}
    스타일: {style_prompts.get(style, style_prompts['informative'])}
    
    스레드 작성 규칙:
    1. 400-450자(공백 포함) 내외로 작성하세요. 정확히 450자를 맞출 필요는 없지만, 내용이 중간에 끊기지 않고 완결되어야 합니다.
    2. 모든 문장은 완전한 문장으로 자연스럽게 끝나야 합니다.
    3. 이모지는 사용하지 마세요.
    4. 반드시 강력한 훅 문장으로 시작하세요! 첫 문장은 스크롤을 멈추게 하는 훅이어야 하며 이것이 가장 중요합니다.
    5. 첫 문장(훅)을 쓴 후에는 반드시 줄바꿈을 하세요.
    
    6. 쓰레드 구조는 다음과 같이 구성하세요:
       A. 강력한 훅 문장 (사람들이 멈춰서 읽게 하는 첫 문장 - 매우 중요!)
       B. 줄바꿈
       C. 상황 설명 또는 공감 유도 문장
       D. 문제 제기 또는 긴장감 조성
       E. 해결책이나 인사이트 제공
       F. 명확한 콜투액션으로 마무리
    
    7. 가독성을 높이는 규칙:
       - 모든 문장은 간결하게 작성하세요. 한 문장은 최대 15자 내외로 짧게 작성하세요.
       - 긴 문장보다는 짧은 문장을 선호하세요.
       - 2-3문장마다 반드시 줄바꿈을 하세요. 이것은 매우 중요합니다.
       - 중요한 문장은 단독으로 한 줄에 배치하세요.
       - 리스트나 강조 표현을 적절히 활용하세요.
       - 부드럽고 친근한 말투로 작성하세요. 딱딱한 문체를 피하세요.
       - 독자와 소통하는 느낌의 글을 작성하세요. 질문을 던지거나 독자의 경험을 떠올리게 하세요.
    
    8. 반드시 마지막에는 명확한 콜투액션으로 마무리하세요.
    {additional_requirements}
    {hook_examples}
    
    {cta_examples}
    
    핵심 규칙:
    - 글은 '잘 쓰는 것'보다 '공감받는 글'이 중요합니다. 사람과 연결되는 글을 작성하세요.
    - 첫 문장은 반드시 강력한 훅으로 시작하고, 그 후 줄바꿈을 하세요.
    - 2-3문장마다 반드시 줄바꿈을 하여 가독성을 높이세요.
    - 정확히 450자를 채울 필요는 없습니다. 자연스럽게 문장이 끝나면 내용을 마무리하세요.
    - 글이 중간에 끊기지 않도록 하세요. 모든 문장은 완결되어야 합니다.
    """

    try:
        print("Calling OpenAI API...")
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 스레드에서 최고의 반응을 얻는 글을 작성하는 전문가입니다. 반드시 강력한 훅으로 시작하고, 첫 문장 후에는 줄바꿈을 하세요. 2-3문장마다 줄바꿈을 해서 가독성을 높이고, 짧고 간결한 문장으로 작성하세요. 부드럽고 친근한 말투로 작성하고, 독자와 소통하는 느낌의 글을 만드세요. 명확한 콜투액션으로 마무리하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,  # 토큰 수 증가
            presence_penalty=0.3,
            frequency_penalty=0.5
        )
        
        content = response.choices[0].message.content
        
        # 생성된 콘텐츠의 글자 수 확인
        char_count = len(content)
        print(f"Generated content ({char_count} characters): {content[:50]}...")
        
        # 글자 수 조정 - 450자 초과시에만 조정
        if char_count > 450:
            print(f"Content exceeds 450 characters ({char_count}), trimming...")
            
            # 글자수가 초과된 경우, 문장이 끝나는 지점에서 자르기
            # 450자 이전에 마지막으로 문장이 끝나는 위치 찾기
            last_sentence_end = max(
                content.rfind('. ', 0, 450),
                content.rfind('! ', 0, 450),
                content.rfind('? ', 0, 450),
                content.rfind('.\n', 0, 450),
                content.rfind('!\n', 0, 450),
                content.rfind('?\n', 0, 450)
            )
            
            if last_sentence_end > 0:
                # 마지막 문장이 끝나는 부분까지 자르기
                content = content[:last_sentence_end+1].strip()
            else:
                # 적절한 문장 끝을 찾지 못한 경우
                content = content[:447] + "..."
        
        # 콜투액션이 없는 경우에만 추가
        has_cta = any(cta in content[-50:].lower() for cta in ['경험', '공유', '댓글', '알려주세요', '어떤가요', '저장', '팔로우', '생각'])
        
        if not has_cta and char_count < 430:
            print("Adding call-to-action...")
            cta_options = [
                f" 여러분의 경험도 댓글로 나눠주세요.",
                f" 이 글이 도움되었다면 저장해두세요.",
                f" 어떻게 생각하시나요?",
                f" 공감한다면 공유해주세요."
            ]
            
            # 가장 짧은 CTA 선택
            cta = min(cta_options, key=len)
            content += cta
        
        print(f"Final content length: {len(content)} characters")
        return content
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"컨텐츠 생성 중 오류가 발생했습니다: {str(e)}"

def revise_content(original_content, revision_prompt, topic, style):
    print(f"Revising content based on revision prompt: {revision_prompt}")
    
    hook_examples = """
    강력한 훅 문장 예시 (첫 문장에 반드시 사용하세요):
    질문형: "왜 대부분의 사람들이 {topic}을 잘못 이해할까요?"
    공감형: "{topic}에 대해 아무도 알려주지 않는 진짜 팁들"
    충격형: "{topic}을 모르면 앞으로 경쟁에서 살아남을 수 없습니다"
    리스트형: "단 3개월 만에 {topic} 마스터한 5가지 방법"
    비밀공개형: "{topic}에 대한 업계의 숨겨진 비밀"
    호기심유발형: "{topic}에 관한 가장 놀라운 사실을 아시나요?"
    관찰형: "요즘 주변을 보면 {topic}에 대한 오해가 너무 많아요"
    공통의 적형: "{topic}때문에 우리 모두 힘들었던 경험 있으시죠?"
    직접경험형: "제가 {topic}을 경험하면서 깨달은 중요한 한 가지"
    """
    
    prompt = f"""
    당신은 쓰레드 콘텐츠 수정 전문가입니다. 기존 글을 사용자의 피드백에 따라 수정해 더 나은 버전을 만드세요.
    
    원본 글:
    ```
    {original_content}
    ```
    
    주제: {topic}
    스타일: {style}
    
    수정 요청사항:
    {revision_prompt}
    
    수정 지침:
    1. 원본 글의 기본 구조와 주제를 유지하면서 수정 요청사항을 반영하세요.
    2. 여전히 400-450자(공백 포함) 내외를 유지하세요.
    3. 반드시 강력한 훅으로 시작하세요! 첫 문장은 스크롤을 멈추게 하는 훅이어야 합니다.
    4. 첫 문장(훅)을 쓴 후에는 반드시 줄바꿈을 하세요.
    5. 문장은 짧고 간결하게, 한 문장은 최대 15자 내외로 작성하세요.
    6. 2-3문장마다 반드시 줄바꿈을 하세요. 이것은 매우 중요합니다.
    7. 부드럽고 친근한 말투로 작성하세요. 딱딱한 문체를 피하세요.
    8. 독자와 소통하는 느낌의 글을 작성하세요. 질문을 던지거나 독자의 경험을 떠올리게 하세요.
    9. 원본보다 더 공감을 얻고 가독성이 높은 글로 만드세요.
    10. 글이 중간에 끊기지 않고 완결되도록 작성하세요.
    11. 명확한 콜투액션으로 마무리하세요.
    
    {hook_examples}
    
    핵심 규칙:
    - 첫 문장은 반드시 강력한 훅으로 시작하고, 그 후 줄바꿈을 하세요.
    - 2-3문장마다 반드시 줄바꿈을 하여 가독성을 높이세요.
    - 모든 문장은 완결되어야 합니다.
    
    전체 수정된 글을 제공해 주세요.
    """
    
    try:
        print("Calling OpenAI API for revision...")
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 스레드에서 최고의 반응을 얻는 글을 수정하는 전문가입니다. 반드시 강력한 훅으로 시작하고, 첫 문장 후에는 줄바꿈을 하세요. 2-3문장마다 줄바꿈을 해서 가독성을 높이고, 짧고 간결한 문장으로 작성하세요. 부드럽고 친근한 말투로 작성하고, 독자와 소통하는 느낌의 글을 만드세요. 명확한 콜투액션으로 마무리하세요."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            presence_penalty=0.3,
            frequency_penalty=0.5
        )
        
        revised_content = response.choices[0].message.content
        
        # 코드 블록 제거 (API가 ```로 둘러싸서 반환할 수 있음)
        if "```" in revised_content:
            revised_content = revised_content.replace("```", "").strip()
        
        # 생성된 콘텐츠의 글자 수 확인
        char_count = len(revised_content)
        print(f"Revised content ({char_count} characters): {revised_content[:50]}...")
        
        # 글자 수 조정 - 450자 초과시에만 조정
        if char_count > 450:
            print(f"Revised content exceeds 450 characters ({char_count}), trimming...")
            
            # 글자수가 초과된 경우, 문장이 끝나는 지점에서 자르기
            last_sentence_end = max(
                revised_content.rfind('. ', 0, 450),
                revised_content.rfind('! ', 0, 450),
                revised_content.rfind('? ', 0, 450),
                revised_content.rfind('.\n', 0, 450),
                revised_content.rfind('!\n', 0, 450),
                revised_content.rfind('?\n', 0, 450)
            )
            
            if last_sentence_end > 0:
                # 마지막 문장이 끝나는 부분까지 자르기
                revised_content = revised_content[:last_sentence_end+1].strip()
            else:
                # 적절한 문장 끝을 찾지 못한 경우
                revised_content = revised_content[:447] + "..."
        
        # 콜투액션이 없는 경우에만 추가
        has_cta = any(cta in revised_content[-50:].lower() for cta in ['경험', '공유', '댓글', '알려주세요', '어떤가요', '저장', '팔로우', '생각'])
        
        if not has_cta and char_count < 430:
            print("Adding call-to-action...")
            cta_options = [
                f" 여러분의 경험도 댓글로 나눠주세요.",
                f" 이 글이 도움되었다면 저장해두세요.",
                f" 어떻게 생각하시나요?",
                f" 공감한다면 공유해주세요."
            ]
            
            # 가장 짧은 CTA 선택
            cta = min(cta_options, key=len)
            revised_content += cta
        
        print(f"Final revised content length: {len(revised_content)} characters")
        return revised_content
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        return f"컨텐츠 수정 중 오류가 발생했습니다: {str(e)}"