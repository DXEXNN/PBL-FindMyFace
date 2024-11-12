from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video, VerificationCode
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import uuid
import os

# Video Upload API
class VideoUploadView(APIView):
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('file')
        video_name = request.data.get('video_name')

        if not video_file or not video_name:
            return Response({"error": "Both video file and video name are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a unique video ID
        video_instance = Video(video_name=video_name, file_path=video_file)
        video_instance.save()

        serializer = VideoSerializer(video_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Video List API
class VideoListView(APIView):
    def get(self, request, *args, **kwargs):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        
        # Add MEDIA_URL prefix to file_path for proper access
        for video in serializer.data:
            video['file_path'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, video['file_path']))

        return Response(serializer.data, status=status.HTTP_200_OK)

# Verification Code Check API
@api_view(['GET'])
def get_verification_code(request, input_code):
    verification = get_object_or_404(VerificationCode, verification_code=input_code)
    return Response({
        'user_id': verification.user.id,
        'verification_code': verification.verification_code
    }, status=status.HTTP_200_OK)
    