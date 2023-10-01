"""auth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from ms_identity_web.django.msal_views_and_urls import MsalViews
from django.conf import  settings
from users.views import signUpPageView, loginPageView,homePageView
msal_urls = MsalViews(settings.MS_IDENTITY_WEB).url_patterns()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('signup/', signUpPageView, name='sign up'),
    path('login/', loginPageView, name='Login'),
    path('home/',homePageView,name="Homepage"),

    path(f'{settings.AAD_CONFIG.django.auth_endpoints.prefix}/', include(msal_urls)),
]
