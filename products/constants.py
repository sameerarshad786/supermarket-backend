from django.db import models
from django.utils.translation import gettext_lazy as _


class Condition(models.TextChoices):
    NOT_DEFINED = "not defined", _("Not Defined")
    NEW = "new", _("New")
    USED = "used", _("Used")
    OPEN_BOX = "open box", _("Open Box")
    REFURBISHED = "refurbished", _("Refurbished")
    DEAD = "dead", _("Dead")


class By(models.TextChoices):
    SUPERMARKET = "supermarket", _("Supermarket")
    WISEMARKET = "wisemarket", _("Wisemarket")
    AMAZON = "amazon", _("Amazon")
    EBAY = "ebay", _("Ebay")
    DARAZ = "daraz", _("Daraz")
    ALI_EXPRESS = "ali express", _("Ali Express")
    ALI_BABA = "ali baba", _("Ali Baba")
    OLX = "olx", _("olx")


class ExtractorType(models.TextChoices):
    DATA = "data", _("Data")
    XPATH = "xpath", _("Xpath")
    CSS = "css", _("Css")
    JSON = "json", _("Jon")
    REGEX = "re", _("Regex")
