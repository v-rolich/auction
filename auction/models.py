from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    balance = models.FloatField(default=1000)

    class Meta:
        ordering = ['id']


class CatHedgehog(models.Model):
    breed = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User, related_name='cat_hedgehogs', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class Lot(models.Model):
    pet = models.ForeignKey(CatHedgehog, related_name='lots', on_delete=models.CASCADE)
    price = models.FloatField()
    owner = models.ForeignKey(User, related_name='lots', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


class Bet(models.Model):
    lot = models.ForeignKey(Lot, related_name='bets', on_delete=models.CASCADE)
    rate = models.FloatField()
    owner = models.ForeignKey(User, related_name='bets', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
