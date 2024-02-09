from django.urls import path, include
from . import views


urlpatterns = [
    path("dashboard", views.Dashboard, name="Dashboard"),
    path("end-report", views.EndReportView, name="EndReportView"),
    path("start-report", views.StartReportView, name="StartReportView"),
    path("whether-report", views.WhetherReportView, name="WhetherReportView"),
    path("lhp", views.LhpView, name="LhpView"),
    path("lhp-tambah", views.LhpAddView, name="LhpAddView"),
    path("lhp-hapus/<int:pk>", views.LhpDeleteView, name="LhpDeleteView"),
    path(
        "perolehan/presiden", views.PerolehanPresidenView, name="PerolehanPresidenView"
    ),
    path("perolehan/dprri", views.PerolehanDprRiView, name="PerolehanDprRiView"),
    path("perolehan/dpdri", views.PerolehanDpdRiView, name="PerolehanDpdRiView"),
    path(
        "perolehan/dprdprov", views.PerolehanDprdProvView, name="PerolehanDprdProvView"
    ),
    path(
        "perolehan/dprdkabkota",
        views.PerolehanDprdKabKotaView,
        name="PerolehanDprdKabKotaView",
    ),
    path(
        "perolehan/presiden-hapus/<int:pk>",
        views.PerolehanPresidenDeleteView,
        name="PerolehanPresidenDeleteView",
    ),
    path(
        "perolehan/dprri-hapus/<int:pk>",
        views.PerolehanDprRiDeleteView,
        name="PerolehanDprRiDeleteView",
    ),
    path(
        "perolehan/dpdri-hapus/<int:pk>",
        views.PerolehanDpdRiDeleteView,
        name="PerolehanDpdRiDeleteView",
    ),
    path(
        "perolehan/dprdprov-hapus/<int:pk>",
        views.PerolehanDprdProvDeleteView,
        name="PerolehanDprdProvDeleteView",
    ),
    path(
        "perolehan/dprdkabkota-hapus/<int:pk>",
        views.PerolehanDprdKabKotaDeleteView,
        name="PerolehanDprdKabKotaDeleteView",
    ),
    path("profile-saya", views.UserProfileView, name="UserProfileView"),
    path("profile-saya/pengaaturan", views.PengaturanView, name="PengaturanView"),
]
