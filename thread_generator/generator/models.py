# generator/models.py
# generator/models.py
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    thread_id = models.CharField(max_length=50)
    interests = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.thread_id

class GeneratedThread(models.Model):
    STYLE_CHOICES = [
        ('informative', '정보형'),
        ('funny', '유머형'),
        ('motivational', '동기부여형'),
        ('story', '스토리형'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='threads')
    topic = models.CharField(max_length=200)
    style = models.CharField(max_length=100, choices=STYLE_CHOICES)
    requirements = models.TextField(blank=True, help_text="추가적인 세부 요건 (선택사항)")
    content = models.TextField()
    feedback = models.TextField(blank=True)
    views = models.IntegerField(default=0)  # 추가된 필드
    created_at = models.DateTimeField(auto_now_add=True)
    revised = models.BooleanField(default=False)  # 수정되었는지 여부
    revision_prompt = models.TextField(blank=True, help_text="수정을 위한 피드백")
    revised_content = models.TextField(blank=True)  # 수정된 콘텐츠 저장
    likes = models.IntegerField(default=0)  # 좋아요 수
    dislikes = models.IntegerField(default=0)  # 싫어요 수
    copies = models.IntegerField(default=0)  # 복사 횟수

    def __str__(self):
        return f"{self.topic} ({self.customer.thread_id})"

    @property
    def get_style_display(self):
        style_dict = dict(self.STYLE_CHOICES)
        return style_dict.get(self.style, self.style)

class CopyLog(models.Model):
    thread = models.ForeignKey(GeneratedThread, on_delete=models.CASCADE, related_name='copy_logs')
    copied_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    def __str__(self):
        return f"Copy of {self.thread.topic} at {self.copied_at}"

class ThreadFeedback(models.Model):
    FEEDBACK_CHOICES = [
        ('like', '좋아요'),
        ('dislike', '싫어요'),
    ]

    thread = models.ForeignKey(GeneratedThread, on_delete=models.CASCADE, related_name='thread_feedback')
    feedback_type = models.CharField(max_length=10, choices=FEEDBACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        unique_together = ('thread', 'ip_address')  # 한 IP당 하나의 피드백만 허용
    
    def __str__(self):
        return f"{self.get_feedback_type_display()} for {self.thread.topic} at {self.created_at}"

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.thread_id}의 리뷰 ({self.rating}점)"

# generator/models.py
# generator/models.py
# generator/models.py
from django.db import models

class Thread(models.Model):
    STYLE_CHOICES = [
        ('informative', '💡 정보형'),
        ('funny', '😆 유머형'),
        ('motivational', '🔥 동기부여형'),
        ('story', '📖 스토리형'),
    ]

    thread_id = models.CharField(max_length=50, unique=True)
    topic = models.CharField(max_length=200)
    style = models.CharField(max_length=100, choices=STYLE_CHOICES)
    content = models.TextField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.thread_id} - {self.topic}"

    def get_style_display_name(self):
        return dict(self.STYLE_CHOICES)[self.style]

class ThreadAnalytics(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('thread', 'ip_address')