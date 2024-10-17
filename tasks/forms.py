from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields= ['titulo', 'categoria', 'existe', 'importante']
        widgets = {
            'titulo': forms.TextInput (attrs={'class': 'form-control', 'placeholder': 'Escribe el titulo'}),
            'categoria': forms.TextInput (attrs={'class': 'form-control', 'placeholder':'Escribe la categoria'}),
            'existe': forms.CheckboxInput (attrs={'class': 'form-check-input text-center'}),
            'importante': forms.CheckboxInput (attrs={'class': 'form-check-input m-auto'})

        }
        
        
        