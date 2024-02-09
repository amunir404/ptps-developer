from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (
    User,
    UserPengawasTps,
    UserProfile,
    StartReport,
    EndReport,
    WhetherReport,
)


@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            user_profile = UserProfile.objects.get(user=instance)
            user_profile.save()
        except:
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, "this user is being saved")


@receiver(post_save, sender=UserPengawasTps)
def post_ptps_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        StartReport.objects.create(ptps=instance)
        EndReport.objects.create(ptps=instance)
        WhetherReport.objects.create(ptps=instance)
    else:
        try:
            start_report = StartReport.objects.get(ptps=instance)
            end_report = EndReport.objects.get(ptps=instance)
            whether_report = WhetherReport.objects.get(ptps=instance)
            whether_report.save()
            start_report.save()
            end_report.save()
        except:
            WhetherReport.objects.create(ptps=instance)
            StartReport.objects.create(ptps=instance)
            EndReport.objects.create(ptps=instance)
