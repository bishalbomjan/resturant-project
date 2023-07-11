from django.shortcuts import render,redirect,get_object_or_404 
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import SearchedRestaurant,Restaurant,Image,RestaurantCuisine,Cuisine,Reservation,Ratings,UserProfile
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from .form import ReservationForm,CommentForm,SearchForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from recommend.Recommendation import KNN_RECOMMENDATION
from django.db.models import Avg, F

@login_required
def make_reservation(request,id,slug,user_id):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    images=Image.objects.filter(restaurant=id)[0]
    user=get_object_or_404(User,id=user_id)
    restaurant_cuisines = RestaurantCuisine.objects.filter(restaurant_id=id)
    cuisine_id = [rc.cuisine_id for rc in restaurant_cuisines]
    cuisines = Cuisine.objects.filter(id__in=cuisine_id)
    if request.method == 'POST':
        # Extract reservation data from the request
        form=ReservationForm(request.POST)
        reservation_data = {
            'restaurant': restaurant,
            'user': user,
            'num_guests': request.POST['num_guests'],
            'date': request.POST['date'],
            'time':request.POST['time'],
        }
        # Attempt to create the reservation, handling optimistic locking
        with transaction.atomic():
            restaurant = Restaurant.objects.select_for_update().get(pk=id)
            # if restaurant.is_full():
            #     return redirect('404')
            reservation = Reservation.objects.select_for_update().filter(
                restaurant=restaurant,
                time=reservation_data['time']
            ).first()

            if reservation is None:
                # If no reservation exists for this time slot, create a new one
                reservation_data['version'] = 1
                restaurant.num_bookings+=1
                reservation = Reservation.objects.create(**reservation_data)
                restaurant.save()
            else:
                # Otherwise, update the existing reservation with a new version number
                reservation.num_guests = reservation_data['num_guests']
                reservation.user = reservation_data['user']
                reservation.version = F('version') + 1
                reservation.save()

        # Render the reservation confirmation page
        return render(request, 'reservation/reservation_confirmation.html', {
            'reservation': reservation
            })
    else:
        form = ReservationForm(initial={
            'restaurant': restaurant.id,'user':user_id
            })
        # Render the reservation form
        return render(request, 'reservation/reservation_form.html', {
            'form':form,
            'image':images,
            'restaurant':restaurant,
            'cuisines':cuisines,
            })

# Create your views here.
def home(request):
    # restaurants = Restaurant.objects.all()[:20]
    restaurants=[]
    test = ""
    for i in range(2,100):
        if Restaurant.objects.filter(id=i).exists():
            test=Restaurant.objects.get(id=i)
        restaurants.append(test)
    restaurant_images = Image.objects.select_related('restaurant').filter(restaurant__in=restaurants)
    bool=True
    restaurant_cuisines = RestaurantCuisine.objects.select_related('restaurant').filter(restaurant__in=restaurants)
    cuisine_id = [rc.cuisine_id for rc in restaurant_cuisines]
    cuisines = Cuisine.objects.filter(id__in=cuisine_id)
    last_login=request.session.get('last_login')
    search_form = SearchForm()
    query=None
    results=[]
    if request.method=='GET':
        search_form=SearchForm(request.GET)
        if search_form.is_valid():
            print('inside search')
            search_query = search_form.cleaned_data['search_query']
            per_page=10
            results = Restaurant.objects.annotate(search=SearchVector('name', 'location'),
                    ).filter(search=search_query).annotate(avg_rating=Avg('average_rating'),
                    ).order_by(F('avg_rating').desc())
            paginator=Paginator(results,10)
            page_number=request.GET.get('page',1)            
            try:
                result=paginator.page(page_number)
            except PageNotAnInteger:
                result=paginator.page(1)
            except EmptyPage:
                result = paginator.page(paginator.num_pages)
            current_url = request.get_full_path()
            
            return render(request, 'base/search.html', {'results': result,'search_query':search_query,'current_url':current_url})
    print(last_login)
    return render(request,'base/home.html',{
        'restaurants':restaurants,
        'bool':bool,
        'images':restaurant_images,
        'last_login':last_login,
        'search_form':search_form,
        'one':1,
        'zero':0
        # 'search_form':search_form,
    })
    
@login_required
def rating_submit(request):
    if request.method=='POST':
        restaurant=Restaurant.objects.get(id=request.POST.get('restaurant'))
        restaurant_id=restaurant
        username=request.POST.get('username')
        rating=request.POST.get('rating')
        body=request.POST.get('body')
        # Check if a rating already exists for this restaurant and user
        rating_obj = Ratings.objects.filter(restaurant=restaurant, username=username).first()
        user=User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if rating_obj:
            # Update the existing rating
            latest_rating_date = Ratings.objects.filter(username=user.username).order_by('-created_at').first().created_at
            user_profile.last_rated_date = latest_rating_date
            user_profile.new_rated=False
            user_profile.save()
            rating_obj.rating = rating
            rating_obj.body = body
            rating_obj.save()
            success_message="Updated Rating"
        else:
            # Create a new rating
            rating_obj = Ratings.objects.create(restaurant=restaurant, username=username, rating=rating, body=body)
            success_message = "Thank you for rating this restaurant!"
            user_profile.last_rated_date = timezone.now()
            user_profile.new_rated=True
            user_profile.save()
        return HttpResponse(success_message)
    else:
        return JsonResponse({'failure': True})

def searchbar(request):
    if request.method == "GET":
        search = request.GET.get('search-restaurant')
        result = SearchedRestaurant.objects.all().filter(content__restaurant=search)
        return render(request,'base/searchbar.html',{'result':result})

@login_required
def restaurant_detail(request,slug,id):
    # restaurant=get_object_or_404(Restaurant,slug=slug)
    restaurant=Restaurant.objects.get(slug=slug)
    images=Image.objects.filter(restaurant=restaurant)
    restaurant_cuisines = RestaurantCuisine.objects.filter(restaurant_id=id)
    cuisine_id = [rc.cuisine_id for rc in restaurant_cuisines]
    cuisines = Cuisine.objects.filter(id__in=cuisine_id)
    f_id=int(id)
    userid=request.user.id
    username=request.user.username
    comment_rating=Ratings.objects.filter(restaurant_id=id)
    paginator = Paginator(comment_rating,5)
    page_number=request.GET.get('page',5)
    try:
        comment=paginator.page(page_number)
    except PageNotAnInteger:
        comment=paginator.page(1)
    except EmptyPage:
        comment = paginator.page(paginator.num_pages)
    comment_form=CommentForm(initial={
            'restaurant': restaurant.id,'username':username
            })
    user_profile=UserProfile.objects.get(user_id=userid)
    u_longitude=user_profile.longitude
    u_latitude=user_profile.latitude
    r_longitude=restaurant.longitude
    r_latitude=restaurant.latitude
    Recommendation=KNN_RECOMMENDATION(k=1)
    distance=Recommendation.haversine(lat1=u_latitude,lon1=u_longitude,lat2=r_latitude,lon2=r_longitude)
    # Render the template with the object as context data
    return render(request, 'restaurant_detail/detail.html', {
        'restaurant':restaurant,
        'images':images,
        'cuisines':cuisines,
        'id':f_id,
        'user_id':userid,
        'comment_form':comment_form,
        'comment_rating':comment,
        'bool':True,
        'distance':distance,
        'detail':True
        })
    
    
def search(request):
    
    if request.method=='post':
        query = request.GET.get('q')
        results = Restaurant.objects.filter(name__icontains=query)[:10]
        return render(request, 'base/search.html', {'results': results})
    

