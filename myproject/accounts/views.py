from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    # 회원가입
    def create(self, request):
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': '동일한 이메일이 이미 존재합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'custom_id': user.custom_id,
                'email': user.email,
                'key': user.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 조회 - 이메일로 key 반환
    def retrieve_key(self, request):
        email = request.data.get('email')  # JSON에서 이메일 가져오기
        if not email:
            return Response({'error': '이메일을 제공해야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
            return Response({'key': user.key}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': '사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
