from django.db import models
import uuid

# Video 모델
class Video(models.Model):
    video_id = models.CharField(max_length=255, unique=True)
    video_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='videos/')  # 파일을 업로드할 경로

    def __str__(self):
        return self.video_name

# VerificationCode 모델
class VerificationCode(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # 사용자와 연결
    verification_code = models.CharField(max_length=255, unique=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='verification_codes', null=True, blank=True)

    def __str__(self):
        return f"Verification Code: {self.verification_code}"

# Search 모델
class Search(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # 사용자가 검색한 기록
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # 검색된 동영상
    search_date = models.DateTimeField(auto_now_add=True)  # 검색한 날짜와 시간 기록

    def __str__(self):
        return f"{self.user.username} searched for {self.video.video_name} on {self.search_date}"

class Result(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # 비디오와 연결
    verification_code = models.ForeignKey(VerificationCode, on_delete=models.CASCADE, null=True, blank=True)  # 검증 코드와 연결 (선택적)
    result_data = models.TextField()  # 결과 데이터를 저장할 필드
    created_at = models.DateTimeField(auto_now_add=True)  # 결과 생성 날짜

    def __str__(self):
        return f"Result for {self.video.video_name} at {self.created_at}"