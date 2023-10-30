from django import forms
from django.contrib import admin
from .models import Receta, Ingrediente, Paso
from django.forms.models import inlineformset_factory

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ["nombre", "cantidad", "unidad"]

class PasoForm(forms.ModelForm):
    class Meta:
        model = Paso
        fields = ["numero", "explicacion"]



class RecetaForm(forms.ModelForm):
    IngredienteFormSet = inlineformset_factory(Receta, Ingrediente , form=IngredienteForm, extra=1)
    PasoFormSet = inlineformset_factory(Receta, Paso , form=PasoForm, extra=1)
    slug = forms.SlugField(max_length=200)
    class Meta:
        model = Receta
        #fields = ["nombre"]
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    

