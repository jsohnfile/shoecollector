from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Store(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('stores_detail', kwargs={'pk':self.id})

class Shoe(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    year = models.IntegerField()
    purchased_price = models.IntegerField()
    image_url = models.CharField(max_length=200, default='https://i.pinimg.com/originals/c4/ce/87/c4ce878870d075fcda7b6a40114f1757.gif')
    stores = models.ManyToManyField(Store)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'shoe_id': self.id})
    
class Recently_Sold(models.Model):
    date = models.DateField('sold date')
    sold_price = models.IntegerField()
    shoe = models.ForeignKey(
        Shoe,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f"{self.sold_price} on {self.date}"

    class Meta:
        ordering = ['-date']