from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.core.mail import send_mail
from .models import Receta, Ingrediente, Paso
from .forms import RecetaForm, PasoForm, IngredienteForm
from .admin import RecetaAdmin


# Create your views here.

def home(request):
    context = {
        "recetas" : Receta.objects.all()

    }
    return render(request, "home.html", context=context)


def contacto(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get("email")
        mensaje = request.POST.get("mensaje")
        mensaje_html = "Email: {} Mensaje: {}".format(email, mensaje)
        send_mail("Contacto de recetas", 
                mensaje_html,
                email,
                ["nachog.akd@gmail.com"],
                fail_silently=False
                )
    return render(request, "contacto.html", context)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #ahora verificamos si el ussuario y contraseña existe y luego entra a la url
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            #si el ususario o contraseña son incorrectos, recarga la pagina con un mensaje de error
            error_message = "Usuario o Contraseña incorrecta"
            return render(request, "registration/login.html", {'error_message' : error_message})
    return render(request, "registration/login.html", {})



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect("/")
    
    return render(request, "registration/register.html", {})

def logout_view(request):
    logout(request)
    return redirect("/")


"""def receta_view(request, slug):
    receta = Receta.objects.get(slug=slug)
    #receta = get_object_or_404(Receta, slug=receta_slug)
    contexto = {
        "receta": receta
    }
    return render(request, "receta.html", context=contexto)"""
def receta_view(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    
    return render(request, 'receta.html', {'receta': receta})    


def receta_nueva(request):
    if request.method == "POST":
        Receta_form = RecetaForm(request.POST)

        Ingrediente_FormSet = IngredienteForm(request.POST, prefix="ingredientes")
        Paso_FormSet = PasoForm(request.POST, prefix="pasos")
        if Receta_form.is_valid() and Ingrediente_FormSet.is_valid() and Paso_FormSet.is_valid():
            receta = Receta_form.save()
            Ingrediente_FormSet.instance = receta
            Ingrediente_FormSet.save()
            Paso_FormSet.instance = receta
            Paso_FormSet.save()
            return redirect("/home")
    else:
        Receta_form = RecetaForm()  
        Ingrediente_FormSet = IngredienteForm(prefix="ingredientes")
        Paso_FormSet = PasoForm(prefix="pasos")  
    return render(request, "recetanueva.html", {"Receta_form": Receta_form,"Ingrediente_FormSet" :Ingrediente_FormSet, "Paso_FormSet": Paso_FormSet})