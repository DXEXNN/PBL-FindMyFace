import os
import random
import string
import pickle
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import FaceEncodingFile, VideoPlatformResult  # 모델 임포트
from .utils import detect_face, extract_features  # 유틸리티 함수
from django.views.decorators.csrf import csrf_exempt  # CSRF 비활성화 데코레이터

def generate_key_test_page(request):
    """
    테스트 키 생성 페이지를 렌더링합니다.
    """
    return render(request, 'face_search/test_generate_key.html')

@csrf_exempt
def create_face_key(request):
    """
    얼굴 이미지 키 생성 및 SQLite 저장
    """
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        if len(files) < 10:
            return JsonResponse({"error": "At least 10 images are required."}, status=400)

        embeddings = []
        random_key = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        try:
            # 파일 처리
            for file in files:
                unique_filename = f"{random_key}_{file.name}"  # 고유 파일 이름 생성
                temp_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
                print(f"Saving temporary file to: {temp_path}")

                # 디렉토리 생성 확인
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                # 파일 저장
                with open(temp_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                # 저장된 파일 경로 확인
                if not os.path.exists(temp_path):
                    raise ValueError(f"File not found at path: {temp_path}")

                # 얼굴 검출 및 특징 추출
                face = detect_face(temp_path)
                if face is not None:
                    print("Face detected successfully.")
                    embedding = extract_features(face)
                    embeddings.append(embedding)
                else:
                    print(f"Face not detected in {file.name}")
                    raise ValueError(f"Face not detected in {file.name}")

            if len(embeddings) != 10:
                raise ValueError("Failed to process all images.")

            # 랜덤 키 생성
            output_path = os.path.join(settings.MEDIA_ROOT, 'face_encodings', f"{random_key}.pkl")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)  # face_encodings 디렉토리 생성
            print(f"Saving embeddings to pickle file: {output_path}")

            # 피클 파일 저장
            with open(output_path, 'wb') as f:
                pickle.dump(embeddings, f)

            return JsonResponse({
                "key": os.path.basename(output_path),
                "message": "Key successfully generated and saved."
            })

        except ValueError as e:
            print(f"ValueError: {e}")
            return JsonResponse({"error": str(e)}, status=400)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
