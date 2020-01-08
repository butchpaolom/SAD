from django.db import models

# Create your models here.


class FrontAsset(models.Model):
    car_img1 = models.ImageField(null=True, blank=False)
    car_img2 = models.ImageField(null=True, blank=True)
    car_img3 = models.ImageField(null=True, blank=True)
    about = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    address = models.TextField()

    def __str__(self):
        return "Front End Assets"
