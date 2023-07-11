from django.urls import path
from . import views

urlpatterns = [
    path('recommend/<int:id>/<int:mtd>/',views.recommend,name='recommend')
]
