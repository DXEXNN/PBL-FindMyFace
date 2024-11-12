"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myproject.accounts.views import UserViewSet


user_lookup = UserViewSet.as_view({
    'get': 'retrieve_key'
})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 회원가입 페이지
    path('accounts/register', UserViewSet.as_view({'post': 'create'}), name='user-register'),  # 회원가입

    # 회원 조회 페이지: 존재하지 않는 이메일일 경우 회원가입 페이지로 리다이렉트
    path('accounts/lookup/', user_lookup, name='user-lookup'),
    
    # video_platform 앱의 URL 연결
    path('video_platform/', include('myproject.video_platform.urls')),  # video_platform 관련 API
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
