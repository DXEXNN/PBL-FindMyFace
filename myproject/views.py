from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def find_my_face(request):
    return render(request, 'find_my_face.html')

def upload(request):
    return render(request, 'upload.html')

def register_page(request):
    return render(request, 'register.html')
