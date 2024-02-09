from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import random
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Prefetch
from perolehansuara.models import CekPpwp, PpwpMedia
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
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                fullname=fullname, email=email, password=password
            )
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
            ptps.provinsi = p_form.cleaned_data["provinsi"]
            ptps.kabkota = p_form.cleaned_data["kabkota"]
            ptps.kecamatan = p_form.cleaned_data["kecamatan"]
            ptps.keldesa = p_form.cleaned_data["keldesa"]
            ptps.tps = p_form.cleaned_data["tps"]
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

    return render(request, "bawaslu/perolehan-presiden.html", context)


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

    return render(request, "bawaslu/perolehan-presiden-kecamatan.html", context)


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

    return render(request, "bawaslu/perolehan-presiden-details.html", context)


def PerolehanPresidenUnduhView(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="laporan.pdf"'

    # Mengambil data dari database
    gambar_data = PpwpMedia.objects.all()

    # Membuat PDF dengan ReportLab
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(100, 800, "Laporan Gambar Dinamis")

    y = 750
    for gambar in gambar_data:
        # Mendapatkan path file gambar
        path_gambar = gambar.images.path

        # Menambahkan gambar dari database ke PDF
        p.drawImage(path_gambar, 100, y, width=200, height=200)
        y -= 220

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
