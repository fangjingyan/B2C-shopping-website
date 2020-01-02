"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from haystack.generic_views import SearchView
from dailyfresh.search_views import GoodsSearchView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^tinymce/', include('tinymce.urls')),
    # re_path(r'^search', include('haystack.urls')),
    re_path(r'^search', GoodsSearchView.as_view(), name='haystack_search'),
    re_path(r'^user/', include('user.urls'), name='user'),
    re_path(r'^order/', include('order.urls'), name='order'),
    re_path(r'^cart/', include('cart.urls'), name='cart'),
    re_path(r'^', include('goods.urls'), name='goods'),
]
