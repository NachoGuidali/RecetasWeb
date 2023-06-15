from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify



class Receta(models.Model):
    # esto es el nombre que va a tener la receta
    nombre = models.CharField(max_length=300)
    #esto va a unir una receta con el usuario que la cargue, pero si se borra el usuario la receta va a seguir estando
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    # aca se va a guardar la fecha en la que se creo la receta
    created_at = models.DateTimeField(auto_now_add=True)
    # aca se guarda lka fecha de modificacion
    update_at = models.DateTimeField(auto_now=True)


    #vamos a agregar el campo SLUG para la url
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        # el slugify genera el slug a partir del parametro nombre en este caso 
        self.slug = slugify(self.nombre)
        super(Receta, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    

#los ingredientes los guardamos en un modelo aparte

class Ingrediente(models.Model):
#primero le especificamos las unidades de los ingredientes   
    UNIDADES = [
        ("unidades", "unidades"),
        ("litros", "litros"),
        ("mililitros", "mililitros"),
        ("cucharadas", "cucharadas"),
        ("gramos", "gramos"),
        ("kilos", "kilos"),

        ]

    nombre = models.CharField(max_length=300)
    cantidad = models.IntegerField(default=1)
    #aca le especificamos que tome del listado de UNIDADES 
    unidad = models.CharField(max_length=20, choices=UNIDADES, default="unidades")
    #aca lo unimos con el modelo de Receta con la palabra ingredientes, y el cascade hace que al borrar una receta se borren sus ingredientes tambien
    receta = models.ForeignKey(Receta, related_name="ingredientes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Paso(models.Model):
    numero = models.IntegerField(default=1)
    explicacion = models.TextField()

    receta = models.ForeignKey(Receta, related_name="paso", on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)       