from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.mixins import UUID
from .user_model import User


def profile_photo_path(instance, filename):
    return f"profile/{instance.id}/{filename}"


class Profile(UUID):
    class Gender(models.TextChoices):
        MALE = ("male", _("Male"))
        FEMALE = ("female", _("Female"))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    image = models.ImageField(upload_to=profile_photo_path, blank=True)

    def update_image(self):
        if self.gender == Profile.Gender.MALE:
            self.image = "profile/default/male.png"
        else:
            self.image = "profile/default/female.png"
        self.save()
