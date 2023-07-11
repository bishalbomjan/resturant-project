from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email=forms.EmailField(max_length=50,required=True)
    number = forms.IntegerField(required=True)
    is_owner=forms.BooleanField(required=False)
    def save(self, commit=True):
        instance = super(UserRegisterForm, self).save(commit=False)
        instance.username = "%s" %(self.cleaned_data['first_name'])
        if commit:
            instance.save()
        return instance
    class Meta:
        model = User
        fields = ['first_name','last_name','email','number','password1','password2','is_owner',]

class LoginForm(AuthenticationForm):
    username=forms.CharField()
    password=forms.CharField()
    latitude=forms.DecimalField()
    longitude=forms.DecimalField()
    class Meta:
        model = User
        fields=['username','password','longitude','latitude']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    