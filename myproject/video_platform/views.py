from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Video, VerificationCode
from .serializers import VideoSerializer
from .forms import VideoUploadForm
from django.http import JsonResponse
from face_search.utils import detect_face, extract_features  # 제공된 FaceNet 유틸리티 사용
import os
import pickle
import cv2
import numpy as np

def match_form_html(request):
    """
    매칭 키 입력용 폼 HTML을 렌더링합니다.
    """
    return render(request, 'video_platform/match_form.html')


def match_videos_html(request):
    """
    사용자 얼굴 키를 기반으로 동영상 매칭 결과를 HTML로 렌더링.
    """
    if request.method == 'POST':
        key = request.POST.get('key')
        if not key:
            return render(request, 'video_platform/match_results.html', {
                "matched_videos": [],
                "error": "Key is required."
            })

        # 키 파일 경로 구성
        key_path = os.path.join(settings.MEDIA_ROOT, 'face_encodings', f"{key}.pkl")
        if not os.path.exists(key_path):
            return render(request, 'video_platform/match_results.html', {
                "matched_videos": [],
                "error": "Key file not found."
            })

        # 키 파일 로드
        try:
            with open(key_path, 'rb') as f:
                user_embeddings = pickle.load(f)
        except Exception as e:
            return render(request, 'video_platform/match_results.html', {
                "matched_videos": [],
                "error": f"Failed to load key file: {str(e)}"
            })

        # 로컬 디렉토리(media/videos)에서 동영상 파일 검색
        videos_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
        video_files = [os.path.join(videos_dir, f) for f in os.listdir(videos_dir) if f.endswith('.mp4')]

        matched_videos = []

        for video_path in video_files:
            matched_frames = 0

            # 동영상 프레임 단위로 처리
            cap = cv2.VideoCapture(video_path)
            fps = int(cap.get(cv2.CAP_PROP_FPS))  # FPS 읽기
            frame_interval = max(fps // 2, 1)  # 초당 2개의 프레임 처리 (최소 1)

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # 특정 간격의 프레임만 처리
                if frame_count % frame_interval == 0:
                    # 프레임에서 얼굴 검출 및 특징점 추출
                    face = detect_face(frame)
                    if face is not None:
                        face_embedding = extract_features(face)

                        # 사용자 특징 벡터와 비교
                        for user_embedding in user_embeddings:
                            similarity = np.linalg.norm(user_embedding - face_embedding)
                            if similarity < 0.6:  # FaceNet 임계값
                                matched_frames += 1

                frame_count += 1
            cap.release()

            if matched_frames > 0:
                matched_videos.append({
                    "video_name": os.path.basename(video_path),
                    "matched_frames": matched_frames
                })

        return render(request, 'video_platform/match_results.html', {
            "matched_videos": matched_videos
        })

    return render(request, 'video_platform/match_results.html', {
        "matched_videos": [],
        "error": "Invalid request method."
    })


def upload_video(request):
    """
    HTML 렌더링을 통해 비디오 업로드를 처리하는 뷰
    """
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_name = form.cleaned_data['video_name']
            video_file = form.cleaned_data['video_file']

            # Video 모델 인스턴스 생성 및 저장
            video = Video.objects.create(
                video_name=video_name,
                file_path=video_file
            )
            return render(request, 'video_platform/upload_success.html', {'video': video})
    else:
        form = VideoUploadForm()

    return render(request, 'video_platform/upload_video.html', {'form': form})

# REST API for Video Upload
class VideoUploadView(APIView):
    """
    Handles video upload via API (JSON request/response).
    """
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('file')
        video_name = request.data.get('video_name')

        # 파일과 비디오 이름이 제공되지 않으면 오류 반환
        if not video_file or not video_name:
            return Response({"error": "Both video file and video name are required."}, status=status.HTTP_400_BAD_REQUEST)

        # 파일을 MEDIA_ROOT 경로에 저장
        video_instance = Video(video_name=video_name, file_path=video_file.name)
        video_instance.save()

        # 파일을 실제 디스크에 저장
        video_path = os.path.join(settings.MEDIA_ROOT, video_file.name)
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        serializer = VideoSerializer(video_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# REST API for Video List
class VideoListView(APIView):
    """
    Handles video list retrieval.
    """
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)

        # 파일 경로에 MEDIA_URL을 추가하여 실제 파일에 접근할 수 있게 함
        for video in serializer.data:
            video['file_path'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, video['file_path']))

        return Response(serializer.data, status=status.HTTP_200_OK)

# REST API for Verification Code
@api_view(['GET'])
def get_verification_code(request, input_code):
    """
    Retrieves verification code details.
    """
    verification = get_object_or_404(VerificationCode, verification_code=input_code)
    return Response({
        'user_id': verification.user.id,
        'verification_code': verification.verification_code
    }, status=status.HTTP_200_OK)
