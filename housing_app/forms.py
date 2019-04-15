
# Forms code retrieved from : https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

from django import forms

from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import fields, CheckboxInput

from .models import UserProfile, Review


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    # first call parent's constructor
        super(UserProfileForm, self).__init__(*args, **kwargs)
    # there's a `fields` property now
        self.fields['avatar'].required = False
    # avatar = forms.ImageField(required=False)
    bio = forms.Textarea()

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.FileInput(
                attrs={
                    'class': 'form-control-file',
                    'style': 'display: none;',
                    'onchange': '$(\'#upload-file-info\').html(this.files[0].name)'
                    }
                ),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control'
                    }
                ),
            }

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    # first call parent's constructor
        super(ReviewForm, self).__init__(*args, **kwargs)
    # there's a `fields` property now
        self.fields['review'].required = True
    review = forms.Textarea()
    
    class Meta:
        model = Review
        fields = ['review',]

