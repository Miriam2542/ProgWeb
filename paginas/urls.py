
from django.urls import path
from .views import Inicio, SobreView
from .views import CategoriaCreate, CategoriaUpdate, CategoriaDelete
from .views import ComentarioCreate, ComentarioUpdate, ComentarioDelete
from .views import NoticiaCreate, NoticiaUpdate, NoticiaDelete
from .views import MidiaCreate, MidiaUpdate, MidiaDelete
from .views import NoticiaList, ComentarioList, MidiaList, CategoriaList
from .views import CadastroUsuarioView
from .views import MinhasNoticias
from .views import NoticiaDetailView
from django.contrib.auth import views as auth_views

from .views import CadastroUsuarioView

 #criar rota registrar para cadastrar novos usuarios

urlpatterns = [
    
    path("registrar/", CadastroUsuarioView.as_view(), name="registrar"),
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
    
    
          
    path("", Inicio.as_view(), name = "index"),
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

    path("listar/categoria/", CategoriaList.as_view(), name="listar-categoria"),
    path("listar/comentario/", ComentarioList.as_view(), name="listar-comentario"),
    path("listar/noticia/", NoticiaList.as_view(), name="listar-noticia"),
    path("listar/midia/", MidiaList.as_view(), name="listar-midia"),

    path("listar/meus-posts/", MinhasNoticias.as_view(), name="listar-noticia"),
    path('noticia/<int:pk>/', NoticiaDetailView.as_view(), name='detalhar-noticia'),
 
]

