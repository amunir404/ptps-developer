from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
import folium
import geocoder
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster
from accounts.models import WhetherReport


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
    location = geocoder.osm("Anggadita")
    lat = location.lat
    lng = location.lng
    country = location

    title_page = "Dashboard Bawaslu"
    whether_list = WhetherReport.objects.all()
    m = folium.Map(location=[-6.34, 107.34], zoom_start=10)
    latitudes = [whether.user_profile.tps.lat for whether in whether_list]
    longitudes = [whether.user_profile.tps.lng for whether in whether_list]

    FastMarkerCluster(data=zip(latitudes, longitudes)).add_to(m)

    m = m._repr_html_()

    context = {
        "title_page": title_page,
        "m": m,
        "whether_list": whether_list,
    }
    return render(request, "bawaslu/dashboard.html", context)
