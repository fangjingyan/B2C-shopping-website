import re
from user.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

# /user/register

'''
# function view
def register(request):
    if request.method == 'Get':
        return render(request, 'register.html')
    else:
        # 1.receive data
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2.verificate data
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': 'incomplete data'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': 'invalid email'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': 'confirm terms'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': 'username already exists'})

        # 3.handle
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 4.return
        return redirect(reverse(views.index))
'''


class RegisterView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 1.receive data
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2.verificate data
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': 'incomplete data'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': 'invalid email'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': 'confirm terms'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': 'username already exists'})

        # 3.handle
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # send activate email containing link http://127.0.0.1:8000/user/active/id
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        subject = 'Dailyfresh Welcome'
        message = ''
        html_message = '<h1>%s, Welcome to Dailyfresh membership</h1> Please click the link to activate your account<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>'%(username, token, token)
        sender = settings.EMAIL_FROM
        recipient_list = [email]
        send_mail(subject, message, sender, recipient_list, html_message=html_message)

        # 4.return
        return redirect(reverse('goods:index'))


class ActiveView(View):

    def get(self, request, token):

        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))

        except SignatureExpired as e:

            return HttpResponse('Activate link is expired')


class LoginView(View):

    def get(self, request):

        return render(request, 'login.html')
