from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreateForm(UserCreationForm):
    '''
    Exposes Email field from User class in order to make it a required field when registering.
    '''
    
    username = forms.RegexField(
        label="UN", max_length=30, regex=r"^[\w.@+-]+$",
        help_text="Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only.",
        error_messages={
            'invalid': "This value may contain only letters, numbers and "
                         "@/./+/-/_ characters."},
        widget=forms.TextInput(attrs={'class': 'form-control',
                                'required': 'true',
                                'placeholder': 'Login'
        })
    )

    password1 = forms.CharField(
        label="PW",
            widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'required': 'true',

        })
    )
    password2 = forms.CharField(
        label="PW",
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'type': 'password',
                                          'required': 'true',
        }),
        help_text="Enter the same password as above, for verification."
    )

    #first_name = forms.CharField(
    #    label="Name",
    #    widget=forms.TextInput(attrs={'class': 'form-control',
    #                                  'type': 'text',
    #                                  'required': 'true',
    #    }),
    #    help_text="Enter user first and last name."
    #)

    email = forms.EmailField(
        required=True, 
        label="EM",
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'type': 'email',
                                      'placeholder': 'Email address',
                                      'required': 'true'
        })
    )
    #email = forms.EmailField(required=True, label='EM')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
