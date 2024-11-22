from django.urls import path
from .views import VideoUploadView, VideoListView, get_verification_code, upload_video, video_list

urlpatterns = [
    path('upload/', upload_video, name='video-upload'),  # 업로드 페이지
    path('list/', video_list, name='video-list'),        # 비디오 목록 페이지
    path('api/upload/', VideoUploadView.as_view(), name='api-video-upload'),  # 동영상 업로드 API
    path('api/list/', VideoListView.as_view(), name='api-video-list'),        # 동영상 목록 API
    path('api/verify/<str:input_code>/', get_verification_code, name='api-get-verification-code'),  # 검증 코드 확인 API
]
