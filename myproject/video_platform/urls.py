from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    upload_video,
    VideoUploadView,
    VideoListView,
    get_verification_code,
    match_videos_html,
    match_form_html,  # 새로운 뷰 추가
)

urlpatterns = [
    path('upload/', upload_video, name='upload-video-html'),  # HTML 렌더링용 URL
    path('upload/api/', VideoUploadView.as_view(), name='video-upload-api'),  # API용 URL
    path('list/', VideoListView.as_view(), name='video-list'),  # 동영상 목록
    path('verify/<str:input_code>/', get_verification_code, name='get-verification-code'),  # 검증 코드 확인
    path('match/html/', match_videos_html, name='match-videos-html'),  # 매칭 결과 HTML
    path('match/form/', match_form_html, name='match-videos-form'),  # 매칭 키 입력용 폼 URL 추가
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
