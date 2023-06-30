"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myapp.views import vip, passbook, report, productlist, products, login_view, api2, change, doing, end
from myapp.views import travel, signout, buy, qrcodes, memberset, modify, ranklist ,daily, service, check
# from myapp.views import signin, signup
from rest_framework.routers import DefaultRouter
from myapp import views

router = DefaultRouter()
router.register(r'myapp', views.myappViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', login_view),
    # path('register/', register, name=""),
    path('api2/', api2, name=""),
    path('member/', vip, name=""),
    # path('signin/', signin, name=""),
    # path('signup/', signup, name=""),
    path('passbook/', passbook, name=""),
    path('question/', report, name=""),
    path('productlist/', productlist, name=""),
    path('daily/', daily, name=""),
    path('travel/', travel, name=""),
    path('products/', products, name=""),
    path('signout/', signout, name=""),
    path('buy/', buy, name=""),
    path('qrcode/', qrcodes, name=""),
    path('memberset/', memberset, name=""),
    path('modify/', modify, name=""),
    path('change/', change, name=""),
    path('doing/', doing, name=""),
    path('end/', end, name=""),
    path('ranklist/', ranklist, name=""),
    path('service/', service, name=""),
    path('check/', check, name=""),
    path('api/', include(router.urls)),
    # path('access/', access, name="")
]
