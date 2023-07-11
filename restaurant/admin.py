from django.contrib import admin
from .models import SearchedRestaurant,Restaurant,RestaurantCuisine,Reservation,Image,Cuisine
# Register your models here.


admin.site.register(SearchedRestaurant)
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display=['name','location','average_rating','number_of_reviews','capacity']
    list_filter=['name','location']
    search_fields=['name','location','capacity']

@admin.register(RestaurantCuisine)
class RestaurantCuisineAdmin(admin.ModelAdmin):
    list_display=['cuisine','restaurant']
    list_filter=['cuisine']
    search_fields=['cuisine__name']
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display=['restaurant','user','date','time']
    list_filter=['date','time']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields=['url']