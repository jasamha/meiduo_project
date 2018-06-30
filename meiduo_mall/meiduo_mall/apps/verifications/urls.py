"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from verifications.views import ImageCodeView, SmsCodeView
from django.conf.urls import url

urlpatterns = [
    url(r'imagecode/(?P<image_code_id>.+)/$', ImageCodeView.as_view()),
    url(r"smscodes/$", SmsCodeView.as_view()),
]
