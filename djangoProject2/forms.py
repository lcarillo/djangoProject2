from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=20, help_text='Inform the phone number.')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].widget.attrs['placeholder'] = '999999999'
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]{9}'
        self.fields['phone_number'].widget.attrs['title'] = 'Número de telefone deve ter 9 dígitos numéricos'

    # Método clean_phone_number para validar o campo phone_number
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        # Aqui você pode adicionar sua própria validação para o número de telefone, se necessário
        return phone_number

    # Sobrescreva o método clean para validar as senhas
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Verifica se as senhas coincidem
        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data
