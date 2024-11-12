from django.urls import path
from .views import VideoUploadView, VideoListView, get_verification_code

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),  # 동영상 업로드
    path('list/', VideoListView.as_view(), name='video-list'),        # 동영상 목록
    path('verify/<str:input_code>/', get_verification_code, name='get-verification-code'),  # 검증 코드 확인
]
