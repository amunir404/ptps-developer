from cProfile import Profile
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.text import get_valid_filename
from django.core.files.storage import default_storage
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
from perolehansuara.models import (
    CekDpdRi,
    CekDprRi,
    CekDprdKabKota,
    CekDprdProv,
    CekPpwp,
    DpdRiMedia,
    DprRiMedia,
    DprdKabKotaMedia,
    DprdProvMedia,
    PpwpMedia,
)
from ptps.forms import (
    EndReportForm,
    LHPForm,
    StartReportForm,
    UserProfileForm,
    WhetherReportForm,
)
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
    whether = get_object_or_404(WhetherReport, ptps=user_pengawas_tps)
    start = get_object_or_404(StartReport, ptps=user_pengawas_tps)
    end = get_object_or_404(EndReport, ptps=user_pengawas_tps)
    whether_form = WhetherReportForm(instance=whether)

    context = {
        "title_page": title_page,
        "start": start,
        "end": end,
        "whether": whether,
        "whether_form": whether_form,
        "user_pengawas_tps": user_pengawas_tps,
    }
    return render(request, "ptps/dashboard.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def StartReportView(request):
    user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
    start = get_object_or_404(StartReport, ptps=user_pengawas_tps)
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
                    f"Pemungutan TPS {user_pengawas_tps.tps} desa {user_pengawas_tps.keldesa} kecamatan {user_pengawas_tps.kecamatan} kabupaten {user_pengawas_tps.kabkota} sudah dimulai",
                )
                return redirect("ptps:Dashboard")
        else:
            print(start_form.errors)
    else:
        start_form = StartReportForm(instance=start)
    return redirect("ptps:Dashboard")


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def WhetherReportView(request):
    user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
    whether = get_object_or_404(WhetherReport, ptps=user_pengawas_tps)
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


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def EndReportView(request):
    user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
    end = get_object_or_404(EndReport, ptps=user_pengawas_tps)
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
                    f"Pemungutan TPS {user_pengawas_tps.tps} desa {user_pengawas_tps.keldesa} kecamatan {user_pengawas_tps.kecamatan} kabupaten {user_pengawas_tps.kabkota} sudah berakhir",
                )
                return redirect("ptps:Dashboard")
        else:
            print(end_form.errors)
    else:
        end_form = EndReportForm(instance=end)
    return redirect("ptps:Dashboard")


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def LhpView(request):
    title_page = "Laporan Hasil Pengawasan"
    lhp_list = Lhp.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "title_page": title_page,
        "lhp_list": lhp_list,
    }
    return render(request, "ptps/lhp.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
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


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
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


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def UserProfileView(request):
    title_page = "Akun Saya"
    user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
    profile = get_object_or_404(UserProfile, user=request.user)
    whether = get_object_or_404(WhetherReport, ptps=user_pengawas_tps)
    start = get_object_or_404(StartReport, ptps=user_pengawas_tps)
    end = get_object_or_404(EndReport, ptps=user_pengawas_tps)

    context = {
        "title_page": title_page,
        "profile": profile,
        "whether": whether,
        "start": start,
        "end": end,
    }
    return render(request, "ptps/user-profile.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PengaturanView(request):
    title_page = "Pengaturan"
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Sudah di Update",
            )
            return redirect("ptps:UserProfileView")
        else:
            print(form.errors)
    else:
        form = UserProfileForm(request.POST, instance=profile)
    context = {
        "title_page": title_page,
        "profile": profile,
        "form": form,
    }
    return render(request, "ptps/pengaturan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanPresidenView(request):
    title_page = "Perolehan Presiden"
    perolehan = PpwpMedia.objects.filter(ptps__user=request.user)
    cek_status = CekPpwp.objects.filter(media__ptps__user=request.user)
    max_foto = 3
    count_foto = max_foto - cek_status.count()

    if request.method == "POST":
        user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
        length = request.POST.get("length")
        for file_num in range(0, int(length)):

            PpwpMedia.objects.create(
                ptps=user_pengawas_tps, images=request.FILES.get(f"images{file_num}")
            )
    context = {
        "title_page": title_page,
        "perolehan": perolehan,
        "count_foto": count_foto,
        "cek_status": cek_status,
    }
    return render(request, "ptps/perolehan-presiden.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDprRiView(request):
    title_page = "Perolehan DPR RI"
    perolehan = DprRiMedia.objects.filter(ptps__user=request.user)
    cek_status = CekDprRi.objects.filter(media__ptps__user=request.user)
    max_foto = 20
    count_foto = max_foto - cek_status.count()

    if request.method == "POST":
        user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
        length = request.POST.get("length")
        for file_num in range(0, int(length)):
            DprRiMedia.objects.create(
                ptps=user_pengawas_tps, images=request.FILES.get(f"images{file_num}")
            )
    context = {
        "title_page": title_page,
        "perolehan": perolehan,
        "count_foto": count_foto,
        "cek_status": cek_status,
    }
    return render(request, "ptps/perolehan-dprri.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDpdRiView(request):
    title_page = "Perolehan DPD RI"
    perolehan = DpdRiMedia.objects.filter(ptps__user=request.user)
    cek_status = CekDpdRi.objects.filter(media__ptps__user=request.user)
    max_foto = 4
    count_foto = max_foto - cek_status.count()

    if request.method == "POST":
        user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
        length = request.POST.get("length")
        for file_num in range(0, int(length)):
            DpdRiMedia.objects.create(
                ptps=user_pengawas_tps, images=request.FILES.get(f"images{file_num}")
            )
    context = {
        "title_page": title_page,
        "perolehan": perolehan,
        "count_foto": count_foto,
        "cek_status": cek_status,
    }
    return render(request, "ptps/perolehan-dpdri.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDprdProvView(request):
    title_page = "Perolehan DPRD Provinsi"
    perolehan = DprdProvMedia.objects.filter(ptps__user=request.user)
    cek_status = CekDprdProv.objects.filter(media__ptps__user=request.user)
    max_foto = 20
    count_foto = max_foto - cek_status.count()

    if request.method == "POST":
        user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
        length = request.POST.get("length")
        for file_num in range(0, int(length)):
            DprdProvMedia.objects.create(
                ptps=user_pengawas_tps, images=request.FILES.get(f"images{file_num}")
            )
    context = {
        "title_page": title_page,
        "perolehan": perolehan,
        "count_foto": count_foto,
        "cek_status": cek_status,
    }
    return render(request, "ptps/perolehan-dprdprov.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDprdKabKotaView(request):
    title_page = "Perolehan DPR Kabupaten Kota"
    perolehan = DprdKabKotaMedia.objects.filter(ptps__user=request.user)
    cek_status = CekDprdKabKota.objects.filter(media__ptps__user=request.user)
    max_foto = 20
    count_foto = max_foto - cek_status.count()

    if request.method == "POST":
        user_pengawas_tps = get_object_or_404(UserPengawasTps, user=request.user)
        length = request.POST.get("length")
        for file_num in range(0, int(length)):
            DprdKabKotaMedia.objects.create(
                ptps=user_pengawas_tps, images=request.FILES.get(f"images{file_num}")
            )
    context = {
        "title_page": title_page,
        "perolehan": perolehan,
        "count_foto": count_foto,
        "cek_status": cek_status,
    }
    return render(request, "ptps/perolehan-dprdkabkota.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanPresidenDeleteView(request, pk=None):
    try:
        perolehan = get_object_or_404(PpwpMedia, pk=pk)

        # Hapus file gambar terkait
        if perolehan.images:
            # Dapatkan path file gambar
            image_path = perolehan.images.path

            # Hapus file gambar dari penyimpanan
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

        # Hapus objek dari database
        perolehan.delete()

        messages.success(request, f"Salah satu Foto berhasil dihapus!")
        return redirect("ptps:PerolehanPresidenView")
    except PpwpMedia.DoesNotExist:
        messages.error(request, f"Maaf Foto tidak ditemukan!")
        return redirect("ptps:PerolehanPresidenView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Foto tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan foto ini!",
        )
        return redirect("ptps:PerolehanPresidenView")


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDprRiDeleteView(request, pk=None):
    try:
        perolehan = get_object_or_404(DprRiMedia, pk=pk)

        # Hapus file gambar terkait
        if perolehan.images:
            # Dapatkan path file gambar
            image_path = perolehan.images.path

            # Hapus file gambar dari penyimpanan
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

        # Hapus objek dari database
        perolehan.delete()

        messages.success(request, f"Salah satu Foto berhasil dihapus!")
        return redirect("ptps:PerolehanDprRiView")
    except DprRiMedia.DoesNotExist:
        messages.error(request, f"Maaf Foto tidak ditemukan!")
        return redirect("ptps:PerolehanDprRiView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Foto tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan foto ini!",
        )
        return redirect("ptps:PerolehanDprRiView")


@login_required(login_url="Login")
@user_passes_test(check_role_pengawastps)
def PerolehanDpdRiDeleteView(request, pk=None):
    try:
        perolehan = get_object_or_404(DpdRiMedia, pk=pk)

        # Hapus file gambar terkait
        if perolehan.images:
            # Dapatkan path file gambar
            image_path = perolehan.images.path

            # Hapus file gambar dari penyimpanan
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

        # Hapus objek dari database
        perolehan.delete()

        messages.success(request, f"Salah satu Foto berhasil dihapus!")
        return redirect("ptps:PerolehanDpdRiView")
    except DpdRiMedia.DoesNotExist:
        messages.error(request, f"Maaf Foto tidak ditemukan!")
        return redirect("ptps:PerolehanDpdRiView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Foto tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan foto ini!",
        )
        return redirect("ptps:PerolehanDpdRiView")


def PerolehanDprdProvDeleteView(request, pk=None):
    try:
        perolehan = get_object_or_404(DprdProvMedia, pk=pk)

        # Hapus file gambar terkait
        if perolehan.images:
            # Dapatkan path file gambar
            image_path = perolehan.images.path

            # Hapus file gambar dari penyimpanan
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

        # Hapus objek dari database
        perolehan.delete()

        messages.success(request, f"Salah satu Foto berhasil dihapus!")
        return redirect("ptps:PerolehanDprdProvView")
    except DprdProvMedia.DoesNotExist:
        messages.error(request, f"Maaf Foto tidak ditemukan!")
        return redirect("ptps:PerolehanDprdProvView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Foto tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan foto ini!",
        )
        return redirect("ptps:PerolehanDprdProvView")


def PerolehanDprdKabKotaDeleteView(request, pk=None):
    try:
        perolehan = get_object_or_404(DprdKabKotaMedia, pk=pk)

        # Hapus file gambar terkait
        if perolehan.images:
            # Dapatkan path file gambar
            image_path = perolehan.images.path

            # Hapus file gambar dari penyimpanan
            if default_storage.exists(image_path):
                default_storage.delete(image_path)

        # Hapus objek dari database
        perolehan.delete()

        messages.success(request, f"Salah satu Foto berhasil dihapus!")
        return redirect("ptps:PerolehanDprdKabKotaView")
    except DprdKabKotaMedia.DoesNotExist:
        messages.error(request, f"Maaf Foto tidak ditemukan!")
        return redirect("ptps:PerolehanDprdKabKotaView")
    except ProtectedError:
        messages.error(
            request,
            f"Maaf Foto tidak dapat dihapus, jika ingin menghapus pastikan tidak ada yang terhubung dengan foto ini!",
        )
        return redirect("ptps:PerolehanDprdKabKotaView")
