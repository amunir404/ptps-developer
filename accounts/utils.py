def detectUser(user):
    if user.role == 1:
        redirectUrl = "bawaslu:Dashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "ptps:Dashboard"
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/login-cms"
        return redirectUrl


def detectProfile(user):
    if user.role == 1:
        redirectUrl = ""
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "ptps:UserProfileView"
        return redirectUrl
