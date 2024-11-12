from django.contrib import admin
from django.urls import path
from myproject.accounts.views import UserViewSet
from django.conf import settings
from django.conf.urls.static import static

# 회원 조회 페이지 (key 조회를 POST 요청으로)
user_lookup = UserViewSet.as_view({
    'post': 'retrieve_key'  # POST 요청으로 변경
})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 회원가입 페이지
    path('accounts/register', UserViewSet.as_view({'post': 'create'}), name='user-register'),  # 회원가입

    # 회원 조회 페이지 (key 조회)
    path('accounts/lookup/', user_lookup, name='user-lookup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
