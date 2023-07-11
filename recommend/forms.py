from django import forms
from restaurant.models import Ratings

class UserPreferenceForm(forms.ModelForm):
    
    class Meta:
        model = Ratings
        fields = ['username','rating','']