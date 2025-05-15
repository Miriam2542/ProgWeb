
from django.urls import path
from .views import Inicio, SobreView

from .views import CategoriaCreate, CategoriaUpdate, CategoriaDelete
from. views import ComentarioCreate, ComentarioUpdate, ComentarioDelete
from. views import NoticiaCreate, NoticiaUpdate, NoticiaDelete
from. views import MidiaCreate, MidiaCreate, MidiaCreate

urlpatterns = [
    
 path("", Inicio.as_view(), name = "index"),
 path("sobre/", SobreView.as_view(), name = "sobre"),
 
 path("adicionar/noticia", ComentarioCreate.as_view()),
 path('adicionar/comentario')
 
]
