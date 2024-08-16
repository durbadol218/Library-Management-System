from django.contrib.auth.forms import UserCreationForm
from .constants import GENDER
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1','password2','birth_date','gender', 'postal_code','city', 'country'] # form a kon kon field thakbe seta define kore dilum!
    
    def save(self,commit=True):
        our_user = super().save(commit=False) # ami database a data save korbo na akhn!
        if commit == True:
            our_user.save() # user model a data save korlam!
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            
            # user object create korlam
            UserProfile.objects.create(
                user = our_user,
                postal_code= postal_code,
                country= country,
                city=city,
                gender= gender,
                birth_date=birth_date,
            )
        return our_user
    
    # aita diye amra inherit korlam userRegistrationForm ke!
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # aita diye amra parent taake overright korlam!!
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
            
