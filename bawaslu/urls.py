from django.urls import path, include
from . import views


urlpatterns = [
    path("dashboard", views.Dashboard, name="Dashboard"),
    path("pengawastps", views.UserPengawasTPSView, name="UserPengawasTPSView"),
    path(
        "perolehan-presiden", views.PerolehanPresidenView, name="PerolehanPresidenView"
    ),
    path(
        "perolehan-presiden/kecamatan/<int:pk>",
        views.PerolehanPresidenKecamatanView,
        name="PerolehanPresidenKecamatanView",
    ),
    path(
        "perolehan-presiden/detail/<int:pk>",
        views.PerolehanPresidenDetailView,
        name="PerolehanPresidenDetailView",
    ),
    path(
        "perolehan-presiden/unduh/<int:pk>",
        views.PerolehanPresidenUnduhView,
        name="PerolehanPresidenUnduhView",
    ),
    path("perolehan-dprri", views.PerolehanDPRRIView, name="PerolehanDPRRIView"),
    path(
        "perolehan-dprri/kecamatan/<int:pk>",
        views.PerolehanDPRRIKecamatanView,
        name="PerolehanDPRRIKecamatanView",
    ),
    path(
        "perolehan-dprri/detail/<int:pk>",
        views.PerolehanDPRRIDetailView,
        name="PerolehanDPRRIDetailView",
    ),
    path("perolehan-dpdri", views.PerolehanDPDRIView, name="PerolehanDPDRIView"),
    path(
        "perolehan-dpdri/kecamatan/<int:pk>",
        views.PerolehanDPDRIKecamatanView,
        name="PerolehanDPDRIKecamatanView",
    ),
    path(
        "perolehan-dpdri/detail/<int:pk>",
        views.PerolehanDPDRIDetailView,
        name="PerolehanDPDRIDetailView",
    ),
    path(
        "perolehan-dprdprov", views.PerolehanDPRDPROVView, name="PerolehanDPRDPROVView"
    ),
    path(
        "perolehan-dprdprov/kecamatan/<int:pk>",
        views.PerolehanDPRDPROVKecamatanView,
        name="PerolehanDPRDPROVKecamatanView",
    ),
    path(
        "perolehan-dprdprov/detail/<int:pk>",
        views.PerolehanDPRDPROVDetailView,
        name="PerolehanDPRDPROVDetailView",
    ),
    path(
        "perolehan-dprdkabkota",
        views.PerolehanDPRDKABKOTAView,
        name="PerolehanDPRDKABKOTAView",
    ),
    path(
        "perolehan-dprdkabkota/kecamatan/<int:pk>",
        views.PerolehanDPRDKABKOTAKecamatanView,
        name="PerolehanDPRDKABKOTAKecamatanView",
    ),
    path(
        "perolehan-dprdkabkota/detail/<int:pk>",
        views.PerolehanDPRDKABKOTADetailView,
        name="PerolehanDPRDKABKOTADetailView",
    ),
]
