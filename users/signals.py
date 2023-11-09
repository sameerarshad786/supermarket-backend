from django.dispatch import receiver
from django.dispatch import Signal

from users.models import Profile


profile_values = Signal(["user", "profile"])


@receiver(profile_values)
def profile_signal(sender, user, profile, **kwargs):
    profile = Profile.objects.create(user=user, **profile)
    Profile.update_image(profile)
    profile.save()
