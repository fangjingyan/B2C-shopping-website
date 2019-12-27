import re
from user.models import User, Address
from goods.models import GoodsSKU
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection
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

# /user/register
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

        send_register_active_email.delay(email, username, token)

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


# user/login
class LoginView(View):

    def get(self, request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'

        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        if not all([username, password]):

            return render(request, 'login.html', {'errmsg': 'incomplete data'})

        user = authenticate(username=username, password=password)

        if user is not None:
            # login() use django session framework to store user_id in the session
            login(request, user)

            next_url = request.GET.get('next', reverse('goods:index'))
            response = redirect(next_url)

            remember = request.POST.get('remember')

            if remember == 'on':
                response.set_cookie('username', username, max_age=7*24*3600)

            else:
                response.delete_cookie('username')

            return response

        else:

            return render(request, 'login.html', {'errmsg': 'user is not active or username or password is wrong'})


# user/logout
class LogoutView(View):

    def get(self, request):
        # clear session
        logout(request)

        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        # get user info
        user = request.user
        address = Address.objects.get_default_address(user)

        # get user history
        # from redis import StrictRedis
        # sr = StrictRedis(host='192.168.2.15', port='6379', db=9)
        # connect redis, history(user_id: sku_id) stored in redis
        con = get_redis_connection('default')
        history_key = 'history_%d'%user.id
        sku_ids = con.lrange(history_key, 0, 4)

        # from db query goods detail
        goods_li = []
        for id in sku_ids:
            good = GoodsSKU.objects.get(id=id)
            goods_li.append(good)

        context = {'page': 'user',
                   'address': address,
                   'goods_li': goods_li}

        return render(request, 'user_center_info.html', context)


# /user/order
class UserOrderView(LoginRequiredMixin, View):

    def get(self, request):

        return render(request, 'user_center_order.html', {'page': 'order'})


# user/address
class AddressView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        #
        # except Address.DoesNotExist:
        #
        #     address = None

        address = Address.objects.get_default_address(user)
        return render(request, 'user_center_site.html', {'page': 'address', 'address': address})

    def post(self, request):
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        if not all([receiver, addr, phone]):

            return render(request, 'user_center_site.html ', {'errmsg': 'incomplete data'})

        # if not re.match(r'^1[3|4|5|7|8][0-9]{9}$]', phone):
        #
        #     return render(request, 'user_center_site.html', {'errmsg': 'invalid phone number'})

        # if there is no default address, then the sumbit address would be default
        user = request.user

        address = Address.objects.get_default_address(user)

        if address:
            is_default = False

        else:
            is_default = True
        print('have data')
        # add address to the database
        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        return redirect(reverse('user:address'))
