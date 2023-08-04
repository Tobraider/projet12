from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    COMMERCIAL = "CO"
    SUPPORT = "SU"
    GESTION = "GE"
    role_choice = (
        (COMMERCIAL, "Commercial"),
        (SUPPORT, "Support"),
        (GESTION, "Gestion"),
    )
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=2, choices=role_choice)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Client(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    tel = PhoneNumberField()
    entreprise = models.CharField(max_length=128)
    time_created = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now_add=True)
    commercial_contact = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)


class Contrat(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    commercial_contact = models.ForeignKey(to=User, on_delete=models.CASCADE)
    prix_ttl = models.FloatField()
    prix_restant = models.FloatField()
    time_created = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField()


class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    contrat = models.ForeignKey(to=Contrat, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    support_contact = models.ForeignKey(to=User, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.CharField(max_length=255)
    attende = models.IntegerField()
    note = models.TextField(max_length=2048)
