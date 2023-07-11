from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_request,name='login'),
    path('signup/<str:isOwner>/',views.signup_request,name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('<int:id>/profile/',views.profile,name='profile'),
    path('<int:id>/edit-profile/<str:username>/',views.edit_profile,name='editprofile'),
]
