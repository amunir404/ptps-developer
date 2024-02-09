from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import User, UserProfile, StartReport, EndReport, WhetherReport


@receiver(post_save, sender=User)
def post_user_created_signal(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        StartReport.objects.create(user=instance)
        EndReport.objects.create(user=instance)
        WhetherReport.objects.create(
            user=instance, user_profile=UserProfile.objects.get(user=instance)
        )
        print(instance.username, "profile is created")
    else:
        try:
            user_profile = UserProfile.objects.get(user=instance)
            start_report = StartReport.objects.get(user=instance)
            end_report = EndReport.objects.get(user=instance)
            whether_report = WhetherReport.objects.get(user=instance)
            user_profile.save()
            start_report.save()
            end_report.save()
            whether_report.save()
        except:
            UserProfile.objects.create(user=instance)
            StartReport.objects.create(user=instance)
            EndReport.objects.create(user=instance)
            WhetherReport.objects.create(user=instance)
            print(instance.username, "profile was not exist, but i created one")


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, "this user is being saved")


# post_save.connect(post_user_created_signal, sender=User)
