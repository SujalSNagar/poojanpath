from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Order

        fields = [

            'full_name',

            'mobile_number',

            'email',

            'address',

            'city',

            'state',

            'postal_code',

            'payment_method',
        ]

        widgets = {

            'full_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter full name',
                    'required': True,

                    'oninvalid': "this.setCustomValidity('Full name is required')",

                    'oninput': "this.setCustomValidity('')"
                }
            ),

            'mobile_number': forms.TextInput(
                attrs={
                    'placeholder': 'Enter mobile number'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                
                    'placeholder': 'Enter email address',

                    'required': True,

                    'oninvalid': "this.setCustomValidity('Email is required')",

                    'oninput': "this.setCustomValidity('')"
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'placeholder': 'Enter full address',

                    'rows': 4
                }
            ),

            'city': forms.TextInput(
                attrs={
                    'placeholder': 'Enter city'
                }
            ),

            'postal_code': forms.TextInput(
                attrs={
                    'placeholder': 'Enter postal code'
                }
            ),

            'payment_method': forms.RadioSelect()
        }


    def clean_mobile_number(self):

        mobile_number = self.cleaned_data[
            'mobile_number'
        ]

        mobile_number = mobile_number.strip()

        if not mobile_number.isdigit():

            raise forms.ValidationError(
                'Mobile number must contain digits only.'
            )

        if len(mobile_number) != 10:

            raise forms.ValidationError(
                'Mobile number must be 10 digits.'
            )

        return mobile_number


    def clean_email(self):
    
        email = self.cleaned_data.get(
            'email'
        )
    
        if not email:
        
            raise forms.ValidationError(
            
                'Email is required.'
            )
    
        return email.lower().strip()


    def clean_postal_code(self):

        postal_code = self.cleaned_data[
            'postal_code'
        ]

        postal_code = postal_code.strip()

        if not postal_code.isdigit():

            raise forms.ValidationError(
                'Postal code must contain digits only.'
            )

        if len(postal_code) != 6:

            raise forms.ValidationError(
                'Postal code must be 6 digits.'
            )

        return postal_code