"""
URL configuration for bawaslu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from core import views
from django.conf import settings
from django.conf.urls.static import static
from ptps.urls import urlpatterns as ptps_urlpatterns
from bawaslu.urls import urlpatterns as bawaslu_urlpatterns

urlpatterns = [
    path("login-cms/", admin.site.urls),
    path("", views.Login, name="Login"),
    path("keluar/", views.Logout, name="Logout"),
    path("dashboard", views.MyDashboard, name="MyDashboard"),
    path("user-profile", views.MyProfile, name="MyProfile"),
    path("help", views.Help, name="Help"),
    path("captcha/", include("captcha.urls")),
    path("ptps/", include((ptps_urlpatterns, "ptps"))),
    path("bawaslu/", include((bawaslu_urlpatterns, "bawaslu"))),
    path("get_kabkota/", views.get_kabkota, name="get_kabkota"),
    path("get_kecamatan/", views.get_kecamatan, name="get_kecamatan"),
    path("get_keldesa/", views.get_keldesa, name="get_keldesa"),
    path("get_tps/", views.get_tps, name="get_tps"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
