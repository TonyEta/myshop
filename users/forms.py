from django import forms 
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Пароль'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Підтвердження пароля'}))

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'Ваш Email'})
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Цей email вже зареєстрований!")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) > 8:
            raise forms.ValidationError("Пароль має містити щонайменше символів")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Паролі не співпадають!")
        return cleaned_data

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'Input', 'placeholder': 'Ваш Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'Input', 'placeholder': 'Пароль'}))