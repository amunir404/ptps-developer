
from accounts.models import UserPengawasTps


def get_ptps(request): 
    try:
        ptps = UserPengawasTps.objects.get(user=request.user)
    except:
        ptps = None
    return dict(vendor=ptps)