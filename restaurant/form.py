from django import forms
from .models import Reservation,Restaurant,Ratings


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'num_guests']
        
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields=['name','location','longitude','latitude','capacity']

class CommentForm(forms.ModelForm):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rating = forms.ChoiceField(choices=RATING_CHOICES)
    class Meta:
        model = Ratings
        fields = ['restaurant','username','rating','body']
    def __str__(self):
        if self.is_valid():
            return f"Rating: {self.cleaned_data['rating']}, Body: {self.cleaned_data['body']}"
        else:
            return f"Invalid form data: {self.errors}"
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=True)
    class Meta:
        fields=['search_query']