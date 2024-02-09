from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
import folium
from accounts.forms import RegisterPengawasTPSForm, RegisterUserForm
from accounts.models import (
    EndReport,
    StartReport,
    User,
    UserPengawasTps,
    UserProfile,
    WhetherReport,
)
from django.http import HttpResponse
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Prefetch
from bawaslu.forms import AccDpdRiForm
from perolehansuara.models import (
    CekDpdRi,
    CekDprRi,
    CekDprdProv,
    CekPpwp,
    DpdRiMedia,
    DprRiMedia,
    DprdProvMedia,
    PpwpMedia,
)
from django.db.models import Count

from wilayah.models import Kecamatan, KelDesa, Tps


# Restrict  accessing the bawaslu prov page
def check_role_bawaslu(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


# Create your views here.
@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def Dashboard(request):
    title_page = "Dashboard Bawaslu"
    user_pengawas = UserPengawasTps.objects.all()
    jk_data = UserProfile.objects.values("jk").annotate(total=Count("jk"))
    labels = [item["jk"] for item in jk_data]
    counts = [item["total"] for item in jk_data]
    whether_list = WhetherReport.objects.all()
    start_list = StartReport.objects.all()
    count_tps = Tps.objects.all().count()
    count_keldesa = KelDesa.objects.all().count()
    count_kec = Kecamatan.objects.all().count()
    m = folium.Map(location=[-6.34, 107.34], zoom_start=10)
    m_tps = folium.Map(location=[-6.34, 107.34], zoom_start=10)
    for start in start_list:
        if start.start_date == True:
            color = "green"
        else:
            color = "red"
        radius = 10
        folium.CircleMarker(
            location=[start.ptps.tps.lat, start.ptps.tps.lng],
            radius=radius,
            color=color,
            stroke=False,
            fill=True,
            fill_opacity=0.5,
            opacity=1,
            popup=f"Desa {start.ptps.keldesa} No TPS {start.ptps.tps}  <br> <a target='_blank' href='https://wa.me/{start.ptps.userprofile.wa}'>Hubungi</a>",
            tooltip=f"Sudah Dimulai",
        ).add_to(m_tps)

    m_tps = m_tps._repr_html_()

    for whether in whether_list:
        # Assigning colors based on status
        if whether.status == WhetherReport.CERAH:
            color = "cornflowerblue"
        elif whether.status == WhetherReport.MENDUNG:
            color = "grey"
        elif whether.status == WhetherReport.HUJAN:
            color = "red"
        else:
            color = "white"  # Default color for unknown status
        radius = 10
        folium.CircleMarker(
            location=[whether.ptps.tps.lat, whether.ptps.tps.lng],
            radius=radius,
            color=color,
            stroke=False,
            fill=True,
            fill_opacity=0.5,
            opacity=1,
            popup=f"Desa {whether.ptps.keldesa} No TPS {whether.ptps.tps}  <br> <a target='_blank' href='https://wa.me/{whether.ptps.userprofile.wa}'>Hubungi</a>",
            tooltip=f"{whether.get_status_display()}",
        ).add_to(m)

    m = m._repr_html_()

    context = {
        "title_page": title_page,
        "m": m,
        "m_tps": m_tps,
        "whether_list": whether_list,
        "user_pengawas": user_pengawas,
        "count_tps": count_tps,
        "count_keldesa": count_keldesa,
        "count_kec": count_kec,
        "labels": labels,
        "counts": counts,
    }
    return render(request, "bawaslu/dashboard.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def UserPengawasTPSView(request):
    title_page = "User Pengawas TPS"
    paginator = Paginator(User.objects.filter(role=2).order_by("created_at"), 100)
    try:
        page_number = int(request.GET.get("page", "1"))
    except:
        page_number = 1
    try:
        ptps = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        ptps = paginator.page(1)
    index = ptps.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    page_range = list(paginator.page_range)[start_index:end_index]
    users = User.objects.filter(role=2)
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        p_form = RegisterPengawasTPSForm(request.POST)
        if form.is_valid() and p_form.is_valid:
            random_number = str(random.randint(1, 9000))
            fullname = form.cleaned_data["fullname"]
            email = form.cleaned_data["email"]
            user = User.objects.create_user(fullname=fullname, email=email)
            user.password = make_password("pemilu2024")
            user.username = (
                user.email.split("@")[0].replace(".", "").replace("-", "")
                + random_number
            )
            user.role = User.PENGAWAS_TPS
            user.is_active = True
            user.save()
            ptps = p_form.save(commit=False)
            ptps.maker = request.user
            ptps.user = user
            userprofile = UserProfile.objects.get(user=user)
            ptps.userprofile = userprofile
            ptps.save()
            return redirect("bawaslu:UserPengawasTPSView")
        else:
            print("invalid form")
            print(form.errors)
    else:
        form = RegisterUserForm()
        s_form = RegisterPengawasTPSForm()

    context = {
        "title_page": title_page,
        "users": users,
        "ptps": ptps,
        "page_range": page_range,
        "form": form,
        "s_form": s_form,
    }
    return render(request, "bawaslu/pengawas-tps-list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanPresidenView(request):
    title_page = "Perolehan Presiden"
    users = UserPengawasTps.objects.all().prefetch_related(
        Prefetch(
            "ppwp",
            queryset=PpwpMedia.objects.all(),
        )
    )
    max_foto = 3
    kecamatans = Kecamatan.objects.all()

    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
    }

    return render(request, "bawaslu/perolehan-presiden/list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanPresidenKecamatanView(request, pk):
    kecamatan = get_object_or_404(Kecamatan, pk=pk)
    title_page = "Perolehan Presiden Kecamatan " + kecamatan.name
    users = UserPengawasTps.objects.filter(kecamatan=kecamatan).prefetch_related(
        Prefetch(
            "ppwp",
            queryset=PpwpMedia.objects.all(),
        )
    )
    max_foto = 3
    kecamatans = Kecamatan.objects.all()
    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
        "kecamatan": kecamatan,
    }

    return render(request, "bawaslu/perolehan-presiden/kecamatan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanPresidenDetailView(request, pk):
    pengawas = get_object_or_404(UserPengawasTps, pk=pk)
    title_page = f"Perolehan Presiden TPS {pengawas.tps} Desa {pengawas.keldesa} Kecamatan {pengawas.kecamatan}"
    whether = get_object_or_404(WhetherReport, ptps=pengawas)
    start = get_object_or_404(StartReport, ptps=pengawas)
    end = get_object_or_404(EndReport, ptps=pengawas)
    media = CekPpwp.objects.filter(media__ptps=pengawas)
    context = {
        "title_page": title_page,
        "pengawas": pengawas,
        "whether": whether,
        "start": start,
        "end": end,
        "media": media,
    }

    return render(request, "bawaslu/perolehan-presiden/details.html", context)


def PerolehanPresidenUnduhView(request, pk):
    user = get_object_or_404(UserPengawasTps, pk=pk)
    media = PpwpMedia.objects.filter(ptps=user)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="C.HASIL-PPWP.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    x_pos = 35
    y_pos = 660

    for image in media:

        img_data = ImageReader(image.images)
        p.drawImage(img_data, x_pos, y_pos, width=600, height=900)
        y_pos -= 250
        if y_pos <= 50:

            p.setFont("Helvetica", 12)
            p.drawString(100, 40, "Halaman berikutnya")
            y_pos = 700
    p.save()
    return response


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRRIView(request):
    title_page = "Perolehan DPR RI"
    users = UserPengawasTps.objects.all().prefetch_related(
        Prefetch(
            "dprri",
            queryset=DprRiMedia.objects.all(),
        )
    )
    max_foto = 20
    kecamatans = Kecamatan.objects.all()

    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
    }

    return render(request, "bawaslu/perolehan-dprri/list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRRIKecamatanView(request, pk):
    kecamatan = get_object_or_404(Kecamatan, pk=pk)
    title_page = "Perolehan DPR RI Kecamatan " + kecamatan.name
    users = UserPengawasTps.objects.filter(kecamatan=kecamatan).prefetch_related(
        Prefetch(
            "dprri",
            queryset=DprRiMedia.objects.all(),
        )
    )
    max_foto = 20
    kecamatans = Kecamatan.objects.all()
    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
        "kecamatan": kecamatan,
    }

    return render(request, "bawaslu/perolehan-dprri/kecamatan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRRIDetailView(request, pk):
    pengawas = get_object_or_404(UserPengawasTps, pk=pk)
    title_page = f"Perolehan DPR RI TPS {pengawas.tps} Desa {pengawas.keldesa} Kecamatan {pengawas.kecamatan}"
    whether = get_object_or_404(WhetherReport, ptps=pengawas)
    start = get_object_or_404(StartReport, ptps=pengawas)
    end = get_object_or_404(EndReport, ptps=pengawas)
    media = CekDprRi.objects.filter(media__ptps=pengawas)
    context = {
        "title_page": title_page,
        "pengawas": pengawas,
        "whether": whether,
        "start": start,
        "end": end,
        "media": media,
    }

    return render(request, "bawaslu/perolehan-dprri/details.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPDRIView(request):
    title_page = "Perolehan DPD RI"
    users = UserPengawasTps.objects.all().prefetch_related(
        Prefetch(
            "dpdri",
            queryset=DpdRiMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()

    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
    }

    return render(request, "bawaslu/perolehan-dpdri/list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPDRIKecamatanView(request, pk):
    kecamatan = get_object_or_404(Kecamatan, pk=pk)
    title_page = "Perolehan DPD RI Kecamatan " + kecamatan.name
    users = UserPengawasTps.objects.filter(kecamatan=kecamatan).prefetch_related(
        Prefetch(
            "dpdri",
            queryset=DpdRiMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()
    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
        "kecamatan": kecamatan,
    }

    return render(request, "bawaslu/perolehan-dpdri/kecamatan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPDRIDetailView(request, pk):
    pengawas = get_object_or_404(UserPengawasTps, pk=pk)
    title_page = f"Perolehan DPD RI TPS {pengawas.tps} Desa {pengawas.keldesa} Kecamatan {pengawas.kecamatan}"
    whether = get_object_or_404(WhetherReport, ptps=pengawas)
    start = get_object_or_404(StartReport, ptps=pengawas)
    end = get_object_or_404(EndReport, ptps=pengawas)
    media = CekDpdRi.objects.filter(media__ptps=pengawas)
    context = {
        "title_page": title_page,
        "pengawas": pengawas,
        "whether": whether,
        "start": start,
        "end": end,
        "media": media,
    }

    return render(request, "bawaslu/perolehan-dpdri/details.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDPROVView(request):
    title_page = "Perolehan DPRD Prov"
    users = UserPengawasTps.objects.all().prefetch_related(
        Prefetch(
            "dprdkabkota",
            queryset=DprdProvMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()

    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
    }

    return render(request, "bawaslu/perolehan-dprdprov/list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDPROVKecamatanView(request, pk):
    kecamatan = get_object_or_404(Kecamatan, pk=pk)
    title_page = "Perolehan DPRD Prov Kecamatan " + kecamatan.name
    users = UserPengawasTps.objects.filter(kecamatan=kecamatan).prefetch_related(
        Prefetch(
            "dprdprov",
            queryset=DprdProvMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()
    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
        "kecamatan": kecamatan,
    }

    return render(request, "bawaslu/perolehan-dprdprov/kecamatan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDPROVDetailView(request, pk):
    pengawas = get_object_or_404(UserPengawasTps, pk=pk)
    title_page = f"Perolehan DPRD Prov TPS {pengawas.tps} Desa {pengawas.keldesa} Kecamatan {pengawas.kecamatan}"
    whether = get_object_or_404(WhetherReport, ptps=pengawas)
    start = get_object_or_404(StartReport, ptps=pengawas)
    end = get_object_or_404(EndReport, ptps=pengawas)
    media = CekDprdProv.objects.filter(media__ptps=pengawas)
    context = {
        "title_page": title_page,
        "pengawas": pengawas,
        "whether": whether,
        "start": start,
        "end": end,
        "media": media,
    }

    return render(request, "bawaslu/perolehan-dprdprov/details.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDKABKOTAView(request):
    title_page = "Perolehan DPRD Kab Kota"
    users = UserPengawasTps.objects.all().prefetch_related(
        Prefetch(
            "dprdkabkota",
            queryset=DprdProvMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()

    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
    }

    return render(request, "bawaslu/perolehan-dprdprov/list.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDKABKOTAKecamatanView(request, pk):
    kecamatan = get_object_or_404(Kecamatan, pk=pk)
    title_page = "Perolehan DPRD Kab Kota Kecamatan " + kecamatan.name
    users = UserPengawasTps.objects.filter(kecamatan=kecamatan).prefetch_related(
        Prefetch(
            "dprdkabkota",
            queryset=DprdProvMedia.objects.all(),
        )
    )
    max_foto = 4
    kecamatans = Kecamatan.objects.all()
    context = {
        "title_page": title_page,
        "users": users,
        "max_foto": max_foto,
        "kecamatans": kecamatans,
        "kecamatan": kecamatan,
    }

    return render(request, "bawaslu/perolehan-dprdprov/kecamatan.html", context)


@login_required(login_url="Login")
@user_passes_test(check_role_bawaslu)
def PerolehanDPRDKABKOTADetailView(request, pk):
    pengawas = get_object_or_404(UserPengawasTps, pk=pk)
    title_page = f"Perolehan DPRD Kab Kota TPS {pengawas.tps} Desa {pengawas.keldesa} Kecamatan {pengawas.kecamatan}"
    whether = get_object_or_404(WhetherReport, ptps=pengawas)
    start = get_object_or_404(StartReport, ptps=pengawas)
    end = get_object_or_404(EndReport, ptps=pengawas)
    media = CekDprdProv.objects.filter(media__ptps=pengawas)
    context = {
        "title_page": title_page,
        "pengawas": pengawas,
        "whether": whether,
        "start": start,
        "end": end,
        "media": media,
    }

    return render(request, "bawaslu/perolehan-dprdprov/details.html", context)


def AccFotoDpdRiView(request, pk):
    user = get_object_or_404(UserPengawasTps, pk=pk)
    form = AccDpdRiForm(request.POST)
    context = {"user": user, "form": form}
    return render(request, "bawaslu/perolehan-dpdri/cek-status.html")
