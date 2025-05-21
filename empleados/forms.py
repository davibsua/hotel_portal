from django import forms
from .models import PostTablon, MensajeChat, Usuario, Departamento
from django.contrib.auth.forms import UserCreationForm
from typing import cast
from django.db.models import QuerySet

class RegistroUsuarioForm(UserCreationForm):
    departamento = forms.ModelChoiceField(
        queryset=cast(QuerySet, Departamento.objects.all()),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", "rol", "departamento")
class PostTablonForm(forms.ModelForm):
    class Meta:
        model = PostTablon
        fields = ["titulo", "cuerpo"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "cuerpo": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class MensajeChatForm(forms.ModelForm):
    class Meta:
        model = MensajeChat
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(attrs={"rows": 2, "class": "form-control", "placeholder": "Escribe tu mensaje…"}),
        }
