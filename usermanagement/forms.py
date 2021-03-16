from django import forms
from usermanagement.models import (UserProfile, UserRole )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name','last_name','email','phone_number','user_role',)

    def __init__(self,*args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].widget.attrs['class'] = "form-control"
            self.fields[key].widget.attrs['required'] = True
        self.fields['user_role'].queryset = UserRole.objects.all()