from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def find_my_face(request):
    return render(request, 'find_my_face.html')

def upload(request):
    return render(request, 'upload.html')


def register_page(request):
    if request.method == "POST":
        email = request.POST.get("email")  # 사용자가 입력한 이메일 가져오기
        # 회원가입 처리 로직 (예: 데이터베이스에 저장 등)
        # 필요한 추가 로직을 여기에 작성

        # 처리 완료 후 리디렉션
        return redirect('/face_search/generate_key_test/')

    # GET 요청일 경우 회원가입 페이지 렌더링
    return render(request, 'register.html')
