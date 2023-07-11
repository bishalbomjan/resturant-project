# Create your views here.
from django.shortcuts import render,get_object_or_404
from restaurant.models import Restaurant,Ratings,UserProfile
from .models import RecommendedRestaurantsUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .Recommendation import KNN_RECOMMENDATION

@login_required
def recommend(request,id,mtd):
    user=get_object_or_404(User,id=id)
    username=user.username
    user_profile=UserProfile.objects.get(user_id=user)
    if mtd==0:
        if Ratings.objects.filter(username=username).exists():
            latest_rating_date = Ratings.objects.filter(username=username).latest('created_at').created_at
            user_profile = UserProfile.objects.get(user_id=id)
            print(user_profile.new_rated)
            if user_profile.new_rated:
                rate=Ratings.objects.filter(username=username).order_by('-created_at').first()
                user_profile.last_rated_date = latest_rating_date
                user_profile.new_rated=False
                user_profile.save()
                rated_restaurant_id=rate.restaurant_id
                rated_restaurant=Restaurant.objects.get(id=rated_restaurant_id)
                rated_restaurant_name=rated_restaurant.name
                Recommendation=KNN_RECOMMENDATION(k=10)
                restaurants_user_ratings=Recommendation.recommend_restaurants_user_ratings(rated_restaurant_name)
                similarity_dict={}
                if RecommendedRestaurantsUser.objects.filter(user_id=id,methods='ratings').exists():
                        RecommendedRestaurantsUser.objects.filter(user_id=id,methods='ratings').delete()
                print('working Inside UserProfileLastRated\n')
                for index, value in restaurants_user_ratings.items():
                    restaurant_name = index                
                    similarity_score = float(value)
                    similarity_dict[restaurant_name] = similarity_score
                    RecommendedRestaurantsUser.objects.create(user=request.user,rated_restaurant=Restaurant.objects.get(name=index),similarity=similarity_score,distance=0,methods='ratings')
                    
                recommend_to_user=RecommendedRestaurantsUser.objects.filter(user_id=request.user.id,methods='ratings').order_by('-similarity')
                return render(request,'recommendation/recommend.html',{
                        'recommend':recommend_to_user,
                        'similarity_calculated_to':rate.restaurant,
                        'bool':False
                    })
            else:
                print('working After Else of RatingObjectS\n')
                if RecommendedRestaurantsUser.objects.filter(user_id=id,methods='ratings').exists():
                    Ratings.objects.filter(username=username)
                    rate=Ratings.objects.filter(username=username).order_by('-created_at').first()
                    print(rate.restaurant)
                    recommend_to_user=list()
                    recommended_restaurants=RecommendedRestaurantsUser.objects.filter(user_id=request.user.id,methods='ratings').order_by('-similarity')
                    print('Inside RecommendedRestaurant')
                    
                    return render(request,'recommendation/recommend.html',{
                        'recommend':recommended_restaurants,
                        'similarity_calculated_to':rate.restaurant,
                        'bool':False
                        }) 
                else:
                    print('Else Recommended Restaurants')
                    recommend_to_user=Restaurant.objects.all().order_by('-number_of_reviews').order_by('-average_rating')
                    return render(request,'recommendation/recommend.html',{
                    'recommend':recommend_to_user[:10],
                    'bool':False,
                    'first':True
                })
                    pass
        else:
            recommend_to_user=Restaurant.objects.all().order_by('-number_of_reviews').order_by('-average_rating')
            return render(request,'recommendation/recommend.html',{
                    'recommend':recommend_to_user[:10],
                    'first':True,
                    'bool':False
                })

