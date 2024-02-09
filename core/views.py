from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.forms import LoginForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import detectProfile, detectUser
from wilayah.models import KabKota, Kecamatan, KelDesa, Tps


def Login(request):
    title_page = "Masuk"
    if request.user.is_authenticated:
        messages.warning(request, "Kamu sudah masuk!")
        return redirect("MyDashboard")
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # Verifying reCAPTCHA
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Anda sekarang masuk.")
                return redirect("MyDashboard")
            else:
                messages.error(request, "Invalid login credentials")

    else:
        form = LoginForm()
    context = {
        "title_page": title_page,
        "form": form,
    }
    return render(request, "guests/login.html", context)


def Logout(request):
    auth.logout(request)
    messages.info(request, "Anda telah keluar.")
    return redirect("Login")


@login_required(login_url="Login")
def MyDashboard(request):
    user = request.user
    redirectURL = detectUser(user)
    return redirect(redirectURL)


def get_kabkota(request):
    provinsi_id = request.GET.get("provinsi_id")
    kabkota = KabKota.objects.filter(provinsi_id=provinsi_id).values("id", "name")
    return JsonResponse(list(kabkota), safe=False)


def get_kecamatan(request):
    kabkota_id = request.GET.get("kabkota_id")
    kecamatan = Kecamatan.objects.filter(kabkota_id=kabkota_id).values("id", "name")
    return JsonResponse(list(kecamatan), safe=False)


def get_keldesa(request):
    kecamatan_id = request.GET.get("kecamatan_id")
    keldesa = KelDesa.objects.filter(kecamatan_id=kecamatan_id).values("id", "name")
    return JsonResponse(list(keldesa), safe=False)


def get_tps(request):
    keldesa_id = request.GET.get("keldesa_id")
    notps = Tps.objects.filter(keldesa_id=keldesa_id).values("id", "no")
    return JsonResponse(list(notps), safe=False)


@login_required(login_url="Login")
def MyProfile(request):
    user = request.user
    redirectURL = detectProfile(user)
    return redirect(redirectURL)


def Help(request):
    title_page = "Pusat Bantuan"
    context = {
        "title_page": title_page,
    }
    return render(request, "guests/pusat-bantuan.html", context)
