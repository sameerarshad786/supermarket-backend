from django.dispatch import receiver
from django.dispatch import Signal

from users.models import Profile


profile_values = Signal(["user", "profile"])


@receiver(profile_values)
def create_profile_signal(sender, user, profile, **kwargs):
    profile = Profile(user=user, **profile)
    if profile.gender == Profile.Gender.MALE:
        profile.image = "profile/default/male.png"
    else:
        profile.image = "profile/default/female.png"
    profile.save()
