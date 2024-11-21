from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video
from .serializers import VideoSerializer
import os

# Video Upload API
class VideoUploadView(APIView):
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

from rest_framework.views import APIView
from .models import Video
from .serializers import VideoSerializer
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings

# Video List API
class VideoListView(APIView):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        
        # 파일 경로에 MEDIA_URL을 추가하여 실제 파일에 접근할 수 있게 함
        for video in serializer.data:
            video['file_path'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, video['file_path']))

        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view
from .models import VerificationCode
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# Verification Code Check API

@api_view(['GET'])
def get_verification_code(request, input_code):
    verification = get_object_or_404(VerificationCode, verification_code=input_code)
    return Response({
        'user_id': verification.user.id,
        'verification_code': verification.verification_code
    }, status=status.HTTP_200_OK)
    