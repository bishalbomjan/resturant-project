from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('searchbar/',views.searchbar,name='searchbar'),
    path('detail/<slug:slug>/<int:id>/', views.restaurant_detail, name='detail'),
    path('reservation/<int:id>/<int:user_id>/<slug:slug>/',views.make_reservation,name='reservation'),
    path('search/',views.search,name='search'),
    path('rating/',views.rating_submit,name='rating_submit')
]