from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import Job

USER_TYPE=(
    ("employer",'Employer'),
    ('jobseeker',"jobseeker")
)

class User_registration(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','password']
    def clean(self):
        clean_data=super().clean()
        password=clean_data.get("password")
        confirm_password=clean_data.get("confirm_password")

        if password!=confirm_password:
            return forms.ValidationError("passwords do no match")
class profileform(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["user_type"]
class JobForm(forms.ModelForm):
    class Meta:
        model=Job
        fields= ['title', 'description',  'company']
