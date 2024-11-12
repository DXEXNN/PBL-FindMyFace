from django.urls import path
from .views import VideoUploadView, VideoListView

urlpatterns = [
    path('upload_video/', VideoUploadView.as_view(), name='upload_video'),  # 영상 업로드 API
    path('videos/', VideoListView.as_view(), name='videos'),  # 업로드된 영상 목록 조회 API
    path('verify/<str:input_code>/', get_verification_code, name='get-verification-code'),
]
