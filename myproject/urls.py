from django.contrib import admin
from django.urls import path, include
from myproject.accounts.views import register_page, UserViewSet
from . import views
user_lookup = UserViewSet.as_view({
    'get': 'retrieve_key'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name='home'),  # 홈 페이지
    path('find-my-face/', views.find_my_face, name='find-my-face'),  # FIND MY FACE
    path('upload/', views.upload, name='upload'),  # UPLOAD
    
    # 회원가입 페이지
    path('accounts/register/', register_page, name='register-page'),  # 회원가입 페이지 렌더링

    # API endpoints
    path('accounts/register-api', UserViewSet.as_view({'post': 'create'}), name='user-register'),  # 회원가입 API
    path('accounts/lookup/', user_lookup, name='user-lookup'),
    
    # video_platform 앱의 URL 연결
    path('video_platform/', include('myproject.video_platform.urls')),  # video_platform 관련 API
]
