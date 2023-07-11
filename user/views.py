from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import UserRegisterForm,EditUserForm,LoginForm
from .models import ownerRestaurant
from restaurant.models import Reservation,RestaurantCuisine,Cuisine,UserProfile
from django.contrib.auth.decorators import login_required
from django.views.defaults import page_not_found
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from collections import defaultdict
from django.utils import timezone
from django.contrib.auth.models import User

def login_request(request):
	if request.user.is_authenticated:
		messages.error(request,"You are already logged in")
		return redirect('homepage')
	else:
		if request.method == "POST":
			form = LoginForm(request, data=request.POST)
			if form.is_valid():
				username = form.cleaned_data.get('username')
				password = form.cleaned_data.get('password')
				latitude=form.cleaned_data.get('latitude')
				longitude=form.cleaned_data.get('longitude')
				print('latitude-longitude')
				print(latitude,longitude)
				user = authenticate(username=username, password=password)
				user_profile = UserProfile.objects.get(user_id=user.id)
				user_profile.latitude = latitude
				user_profile.longitude = longitude
				user_profile.save()
				# last_login=user.last_login
				# if last_login is None:
				# 	last_login=True
				# else:
				# 	last_login=False
				# request.session['last_login']=last_login
				is_owner=user.userprofile.is_owner
				if user is not None:
					if is_owner == True:
         
						login(request, user)
						messages.info(request, f"You are now logged in as Owner {username}.")
						return redirect('homepage')
					else:
						login(request,user)
						messages.info(request,f'Logged in as Customer {username}')
						return redirect('homepage')
				else:
					messages.error(request,"Invalid username or password.")
			else:
				messages.error(request,"Invalid username or password.")
	form = LoginForm()
	return render(request=request, template_name="user/login.html", context={
	 "form":form
	 })

def signup_request(request,isOwner):
	if request.method=='POST':
		form = UserRegisterForm(data=request.POST)
		if form.is_valid():
			form_f=form.save()
			user=User.objects.get(username=form_f.first_name)
			print(user.id)
			print(timezone.now())
			if isOwner == 'owner_signup':
				UserProfile.objects.create(user=user,is_owner=True,last_rated_date=timezone.now(),new_rated=False)
			elif isOwner == 'customer_signup':
				print(isOwner)
				UserProfile.objects.create(user=user,is_owner=False,last_rated_date=timezone.now(),new_rated=False)
			email=form.cleaned_data.get('email')
			messages.success(request,f'Account created for {email}.')
			return redirect('login')
		else:
			messages.error(request,f'Error occured while Signing up')				
			return redirect(reverse('signup', args=[isOwner]))
	else:			
		form_f = UserRegisterForm()
		if isOwner=='owner_signup':
			bool=True
		elif isOwner =='customer_signup':
			bool=False
		else:
			return page_not_found(request, exception=None, template_name='error/404.html')
		return render(request,'user/signup.html',context={
			'form':form_f,
			'bool':bool,
			})
	
# @login_required
# def preferences(request):
#     pass

@login_required
def profile(request,id):
	user_profile=get_object_or_404(UserProfile,user=id)
	is_owner=user_profile.is_owner
	print(is_owner)
	if is_owner:
		owner=get_object_or_404(ownerRestaurant,owner=id)
		print(owner.restaurant.id)
		reserve=Reservation.objects.filter(restaurant_id=owner.restaurant.id)
		restaurant_cuisines = RestaurantCuisine.objects.filter(restaurant_id=owner.restaurant.id)
		cuisine_id = [rc.cuisine_id for rc in restaurant_cuisines]
		cuisines = Cuisine.objects.filter(id__in=cuisine_id)
		print(owner.restaurant.name)
		return render(request,'user/profile.html',{
		'owner':owner,
		'is_owner':is_owner,
		'cuisines':cuisines,
		'reservation':reserve,
		})
	else:
		reserve=Reservation.objects.filter(user=id)
		return render(request,'user/profile.html',{
		'reservation':reserve,
		'is_owner':is_owner,
		'user_profile':user_profile
		})

@login_required
def logout_view(request):
	logout(request)
	return redirect('login')

@login_required
def edit_profile(request,id,username):
	if request.method=='POST':
		form = EditUserForm(request.POST,instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request,'Successfully updated Profile Details')
			return redirect('profile',id=id)
	else:
		form = EditUserForm(instance=request.user)
	return render(request,'user/edit_profile.html',{
		'form':form
	})
 