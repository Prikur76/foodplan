from django import forms

from customers.models import Customer


class AuthForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        required=True, label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Customer
        fields = ['email', 'password']


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        required=True, label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        required=True, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        required=True, label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        required=True, label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже зарегистрирован')
        return email
