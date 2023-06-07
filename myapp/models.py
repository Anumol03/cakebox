from django.db import models

# Create your models here.
class Cake(models.Model):
    name=models.CharField(max_length=250)
    flavour=models.CharField(max_length=200)
    price=models.PositiveBigIntegerField()
    shape=models.CharField(max_length=250)
    weight=models.CharField(max_length=200)
    layer=models.PositiveIntegerField()
    pic=models.ImageField(upload_to="images",null=True,blank=True)
    def __str__(self):
        return self.name



