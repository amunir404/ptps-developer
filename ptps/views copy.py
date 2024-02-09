from cProfile import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from accounts.models import (
    EndReport,
    StartReport,
    User,
    UserPengawasTps,
    UserProfile,
    WhetherReport,
)
from django.contrib import messages
from laporanhasil.models import Lhp, LhpMedia
from ptps.forms import EndReportForm, LHPForm, StartReportForm, WhetherReportForm
from django.db.models import ProtectedError


# Restrict  accessing the bawaslu prov page
def check_role_pengawastps(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


# Create your views here.
@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def Dashboard(request):
    title_page = "Dashboard Pengawas TPS"
    user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
    start = get_object_or_404(StartReport, ptps=user_pengawas_tps)
    end = get_object_or_404(EndReport, ptps=request.user)
    profile = get_object_or_404(UserProfile, ptps=request.user)
    whether = get_object_or_404(WhetherReport, ptps=request.user)
    whether_form = WhetherReportForm(instance=whether)
    context = {
        "title_page": title_page,
        "start": start,
        "end": end,
        "whether": whether,
        "whether_form": whether_form,
        "profile": profile,
    }
    return render(request, "ptps/dashboard.html", context)


def StartReportView(request):
    start = get_object_or_404(StartReport, ptps=request.user)
    profile = get_object_or_404(UserProfile, ptps=request.user)
    if request.method == "POST":
        start_form = StartReportForm(request.POST, instance=start)
        if start_form.is_valid():
            if StartReport.objects.filter(start_date=True).exists():
                messages.error(request, "Anda sudah melaporkan")
                return redirect("ptps:Dashboard")
            else:
                start.start_date = True
                start_form.save()
                messages.success(
                    request,
                    f"Pemungutan TPS {profile.tps} desa {profile.keldesa} kecamatan {profile.kecamatan} kabupaten {profile.kabkota} sudah dimulai",
                )
                return redirect("ptps:Dashboard")
        else:
            print(start_form.errors)
    else:
        start_form = StartReportForm(instance=start)
    return redirect("ptps:Dashboard")


def EndReportView(request):
    end = get_object_or_404(EndReport, user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        end_form = EndReportForm(request.POST, instance=end)
        if end_form.is_valid():
            if EndReport.objects.filter(end_date=True).exists():
                messages.error(request, "Anda sudah melaporkan")
                return redirect("ptps:Dashboard")
            else:
                end.end_date = True
                end_form.save()
                messages.success(
                    request,
                    f"Pemungutan TPS {profile.tps} desa {profile.keldesa} kecamatan {profile.kecamatan} kabupaten {profile.kabkota} sudah berakhir",
                )
                return redirect("ptps:Dashboard")
        else:
            print(end_form.errors)
    else:
        end_form = EndReportForm(instance=end)
    return redirect("ptps:Dashboard")


def LhpView(request):
    title_page = "Laporan Hasil Pengawasan"
    lhp_list = Lhp.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "title_page": title_page,
        "lhp_list": lhp_list,
    }
    return render(request, "ptps/lhp.html", context)


def LhpAddView(request):
    title_page = "Tambah Laporan Hasil Pengawasan"
    if request.method == "POST":
        form = LHPForm(request.POST)
        if form.is_valid():
            length = request.POST.get("length")
            tahapan = form.cleaned_data["tahapan"]
            bentuk = form.cleaned_data["bentuk"]
            tujuan = form.cleaned_data["tujuan"]
            sasaran = form.cleaned_data["sasaran"]
            waktu = form.cleaned_data["waktu"]
            tempat = form.cleaned_data["tempat"]
            uraian = form.cleaned_data["uraian"]
            lhp = Lhp.objects.create(
                tahapan=tahapan,
                bentuk=bentuk,
                tujuan=tujuan,
                sasaran=sasaran,
                waktu=waktu,
                tempat=tempat,
                uraian=uraian,
                user=request.user,
            )

            for file_num in range(0, int(length)):
                LhpMedia.objects.create(
                    lhp=lhp, images=request.FILES.get(f"images{file_num}")
                )

    else:
        form = LHPForm(request.POST)

    context = {
        "title_page": title_page,
        "form": form,
    }
    return render(request, "ptps/lhp-tambah.html", context)


def LhpDeleteView(request, pk=None):
    try:
        lhp = get_object_or_404(Lhp, pk=pk)
        lhp.delete()
        messages.success(request, f"LHP  {lhp.tahapan} berhasil di hapus!")
        return redirect("ptps:LhpView")
    except User.DoesNotExist:
        messages.error(request, f"Maaf LHP tidak ada!")
        return redirect("ptps:LhpView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Kategori {lhp.tahapan} tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan kategori ini!",
        )
        return redirect("ptps:LhpView")


def UserProfileView(request):
    title_page = "Akun Saya"
    profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        "title_page": title_page,
        "profile": profile,
    }
    return render(request, "ptps/user-profile.html", context)


def Settings(request):
    title_page = "Pengaturan"
    profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        "title_page": title_page,
        "profile": profile,
    }
    return render(request, "ptps/akun_me.html", context)


def PerolehanPresidenView(request):
    title_page = "Perolehan Presiden"
    context = {
        "title_page": title_page,
    }
    return render(request, "ptps/rekap-presiden.html", context)


def WhetherReportView(request):
    whether = get_object_or_404(WhetherReport, user=request.user)
    if request.method == "POST":
        whether_form = WhetherReportForm(request.POST, instance=whether)
        if whether_form.is_valid():
            whether_form.save()
            messages.success(
                request,
                f"Cuaca Sudah Cerah",
            )
            return redirect("ptps:Dashboard")
        else:
            print(whether_form.errors)
    else:
        whether_form = WhetherReportForm(instance=whether)
    context = {
        "whether": whether,
        "whether_form": whether_form,
    }
    return redirect("ptps:Dashboard", context)
