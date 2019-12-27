from django.urls import path, re_path
from user.views import RegisterView, ActiveView, LoginView, LogoutView, UserInfoView, UserOrderView, AddressView
from django.contrib.auth.decorators import login_required


app_name = 'user'
urlpatterns = [
    re_path(r'^register$', RegisterView.as_view(), name='register'),
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
    re_path('^login$', LoginView.as_view(), name='login'),
    re_path('^logout$', LogoutView.as_view(), name='logout'),
    re_path(r'^$', UserInfoView.as_view(), name='user'),
    re_path(r'^order$', UserOrderView.as_view(), name='order'),
    re_path(r'^address$', AddressView.as_view(), name='address')

]
