from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant
    
class ownerRestaurant(models.Model):
    owner=models.ForeignKey(User,related_name='owner',on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,related_name='owner_restaurant',on_delete=models.CASCADE)
    def __str__(self):
        return self.owner.username



