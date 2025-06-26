
from django.urls import path
from .views import Inicio, SobreView
from .views import CategoriaCreate, CategoriaUpdate, CategoriaDelete
from. views import ComentarioCreate, ComentarioUpdate, ComentarioDelete
from. views import NoticiaCreate, NoticiaUpdate, NoticiaDelete
from. views import MidiaCreate, MidiaUpdate, MidiaDelete
from. views import NoticiaList, ComentarioList, MidiaList, CategoriaList

from django.contrib.auth import views as auth_views

urlpatterns = [
    #criar rota para pagina de login
    path("login/", auth_views.LoginView.as_view(
        template_name = 'paginas/form.html' , extra_context = {
        'titulo': 'Autentificar',
        'botao': 'Entrar',
    }
    ), name="login"),

    #criar rota de logout 
    path("sair/" , auth_views.LogoutView.as_view(), name="logout"),

     path("senha/", auth_views.PasswordChangeView.as_view(
        template_name = 'paginas/form.html' , extra_context = {
        'titulo': 'atualizar senha',
        'botao': 'salvar',
    }
     ), name="senha"),
    
    
          
    path("",Inicio.as_view(), name = "index"),
    path("sobre/", SobreView.as_view(), name = "sobre"),
    
    path("adicionar/noticia/", NoticiaCreate.as_view(), name="adicionar-noticia"),
    path('adicionar/comentario/', ComentarioCreate.as_view(), name="adicionar-comentario"),
    path('adicionar/midia/', MidiaCreate.as_view(), name="adicionar-midia"),
    path('adicionar/categoria/', CategoriaCreate.as_view(), name="adicionar-categoria"),

    path("editar/categoria/<int:pk>/", CategoriaUpdate.as_view(), name="editar-categoria"),
    path("editar/noticia/<int:pk>/", NoticiaUpdate.as_view(), name="editar-noticia"),
    path("editar/comentario/<int:pk>/", ComentarioUpdate.as_view(), name="editar-comentario"),
    path("editar/midia/<int:pk>/", MidiaUpdate.as_view(), name="editar-midia"),

    path("excluir/categoria/<int:pk>/", CategoriaDelete.as_view(), name="excluir-categoria"),
    path("excluir/comentario/<int:pk>/", ComentarioDelete.as_view(), name="excluir-comentario"),
    path("excluir/noticia/<int:pk>/", NoticiaDelete.as_view(), name="excluir-noticia"),
    path("excluir/midia/<int:pk>/", MidiaDelete.as_view(), name="excluir-midia"),

    path("excluir/categoria/<int:pk>/", CategoriaList.as_view(), name="excluir-categoria"),
    path("excluir/comentario/<int:pk>/", ComentarioList.as_view(), name="excluir-comentario"),
    path("excluir/noticia/<int:pk>/", NoticiaList.as_view(), name="excluir-noticia"),
    path("excluir/midia/<int:pk>/", MidiaList.as_view(), name="excluir-midia"),

    path("listar/noticia",NoticiaList.as_view(), name = "listar-noticia"),
    
    
    
    

    
    
 
]
