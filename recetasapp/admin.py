from django.contrib import admin
from .models import Receta, Ingrediente, Paso
from .forms import IngredienteForm, RecetaForm, PasoForm



class PasoInline(admin.TabularInline):
    form = PasoForm
    model = Paso
    extra=0
    

class IngredienteInline(admin.TabularInline):
    form = IngredienteForm
    model = Ingrediente
    extra = 0

class RecetaAdmin(admin.ModelAdmin):
    form = RecetaForm
    inlines = [IngredienteInline, PasoInline]
    list_display = ["nombre", "created_at"]
    prepopulated_fields = {"slug" : ("nombre", "usuario")}

admin.site.register(Receta, RecetaAdmin)