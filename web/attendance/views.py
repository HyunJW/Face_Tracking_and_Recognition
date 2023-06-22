from django.shortcuts import render, redirect
from attendance.models import User
import hashlib


def home(request):
    if 'userid' not in request.session.keys():
        return render(request, 'attendance/login.html')
    else:
        return render(request, 'attendance/main.html')


def login(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        row = User.objects.filter(user_id=user_id, password=password)[0]
        if row is not None:
            request.session['user_id'] = user_id
            request.session['first_name'] = row.first_name
            return render(request, 'attendance/main.html')
        else:
            return render(request, 'attendance/login.html', {'msg': '아이디 또는 비밀번호가 일치하지 않습니다.'})
    else:
        return render(request, 'attendance/login.html')


def join(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        password = hashlib.sha256(password.encode()).hexdigest()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        gender = request.POST['gender']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        profile_picture = request.POST['profile_picture']
        User(user_id=user_id, password=password, first_name=first_name, last_name=last_name, age=age, gender=gender,
             email=email, phone_number=phone_number, address=address, profile_picture=profile_picture).save()
        request.session['user_id'] = user_id
        request.session['first_name'] = first_name
        return render(request, 'attendance/main.html')
    else:
        return render(request, 'attendance/join.html')


def logout(request):
    request.session.clear()
    return redirect('/attendance')
