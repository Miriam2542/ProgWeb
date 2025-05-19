
from django.urls import path
from .views import Inicio, SobreView

from .views import CategoriaCreate, CategoriaUpdate, CategoriaDelete
from. views import ComentarioCreate, ComentarioUpdate, ComentarioDelete
from. views import NoticiaCreate, NoticiaUpdate, NoticiaDelete
from. views import MidiaCreate, MidiaCreate, MidiaCreate

urlpatterns = [
    
    path("", Inicio.as_view(), name = "index"),
    path("sobre/", SobreView.as_view(), name = "sobre"),
    
    path("adicionar/noticia/", NoticiaCreate.as_view(), name="adicionar-noticia"),
    path('adicionar/comentario/', ComentarioCreate.as_view(), name="adicionar-comentario"),
    path('adicionar/midia/', MidiaCreate.as_view(), name="adicionar-midia"),
    path('adicionar/categoria/', CategoriaCreate.as_view(), name="adicionar-categoria"),

    path("editar/categoria/<int:pk>/", CategoriaUpdate.as_view(), name="editar-categoria"),
    
    
 
]
