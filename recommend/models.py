from django.db import models
from django.contrib.auth.models import User
from restaurant.models import Restaurant

# Create your models here.
class UserPreferences(models.Model):
    user=models.ForeignKey(User,related_name='user_pref',on_delete=models.CASCADE)
    rated_restaurant=models.ForeignKey(Restaurant,related_name='rated_restaurant',on_delete=models.CASCADE)
    cuisine=models.CharField(max_length=50,null=True)
    location=models.CharField(max_length=150,null=True)
    latitude=models.FloatField()
    longitude=models.FloatField()
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural='Restaurant'
        
class RecommendedRestaurantsUser(models.Model):
    user=models.ForeignKey(User,related_name='recommended_user',on_delete=models.CASCADE)
    rated_restaurant=models.ForeignKey(Restaurant,related_name='recommended_restaurants',on_delete=models.CASCADE)
    similarity=models.FloatField()
    distance=models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    methods=models.CharField(max_length=10)
    