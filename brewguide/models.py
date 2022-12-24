from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser, models.Model):
    pass

class Location(models.Model):
    name = models.TextField(blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"

class Shop(models.Model):
    name = models.TextField(blank=False, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False, null=False, related_name="shops")
    lunch = models.BooleanField(blank=False, null=False)
    traybakes = models.BooleanField(blank=False, null=False)
    coverImage = models.ImageField(upload_to="brewguide")
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long  = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=False, null=False)


    def __str__(self):
        return f"{self.name}"


class Image(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(upload_to="brewguide")
    

    def __str__(self):
        return f"{self.shop}"


class Review(models.Model):
    content = models.TextField(blank=False, null=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, blank=False, null=False)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f"Review: {self.content} Author: {self.poster}"

class AboutImage(models.Model):
    image = models.ImageField(upload_to="brewguide")
    

    def __str__(self):
        return "aboutImage"