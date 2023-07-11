from django.db import models,transaction
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    longitude=models.FloatField(null=True)
    latitude=models.FloatField(null=True)
    average_rating = models.FloatField()
    number_of_reviews = models.IntegerField()
    capacity=models.IntegerField()
    num_bookings=models.IntegerField(default=10)
    slug=models.SlugField(max_length=250)
    
    
    class Meta:
        verbose_name_plural='Restaurant'
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def is_full(self):
        return self.capacity >= self.num_bookings
    def get_absolute_url(self):
        return reverse("restaurant_detail",args=[self.slug] )

class Image(models.Model):
    url = models.URLField()
    restaurant = models.ForeignKey(Restaurant,related_name="image", on_delete=models.CASCADE)
    image_name=models.CharField(max_length=3000)
    def __str__(self):
        return self.restaurant.name

class Cuisine(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class RestaurantCuisine(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,related_name='restaurant_cuisine')
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE,related_name='cuisine')
    def __str__(self):
        return self.cuisine.name
    
class Reservation(models.Model):
    TIME_CHOICE={
    ("1","11:00")
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,related_name='reserve_restaurant')
    date = models.DateField()
    time = models.TimeField()
    num_guests = models.IntegerField()
    version=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    class Meta:
        unique_together = ('restaurant', 'date', 'time')
        
    
class SearchedRestaurant(models.Model):
    restaurant = models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.restaurant

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE)
    is_owner=models.BooleanField(default=False)
    latitude=models.FloatField(default=0,null=True)
    longitude=models.FloatField(default=0,null=True)
    last_rated_date=models.DateTimeField()
    new_rated=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Ratings(models.Model):
    restaurant = models.ForeignKey(Restaurant,related_name='rating_restaurant',on_delete=models.CASCADE)
    username=models.CharField(max_length=500,null=True)
    rating= models.IntegerField()
    body=models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.username





    