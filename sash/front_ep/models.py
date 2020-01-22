from django.db import models

# Create your models here.


class FrontAsset(models.Model):
    company_logo = models.ImageField(null=True, blank=False)
    company_name = models.CharField(null=True, blank=True, max_length=30)
    car_img1 = models.ImageField(null=True, blank=False)
    car_img2 = models.ImageField(null=True, blank=True)
    car_img3 = models.ImageField(null=True, blank=True)
    about = models.TextField()
    mission = models.TextField()
    vision = models.TextField()
    address = models.TextField()
    colorscheme = models.CharField(max_length=7, default="#222222")

    def __str__(self):
        return "Front End Assets"
