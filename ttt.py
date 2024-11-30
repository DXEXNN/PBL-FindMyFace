import os
from django.conf import settings

# Django 환경 초기화
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  # 'myproject'를 실제 프로젝트 이름으로 바꾸세요
import django
django.setup()

# 테스트 코드
key = "AAAAA"
key_path = os.path.join(settings.MEDIA_ROOT, 'face_encodings', f"{key}.pkl")

print("Key Path:", key_path)
print("File Exists:", os.path.exists(key_path))
