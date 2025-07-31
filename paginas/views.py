from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia, User
from django.views.generic import TemplateView , ListView
 
from django.contrib.auth.mixins import LoginRequiredMixin
#importar a class Noticia
class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView (TemplateView):
    template_name = "paginas/sobre.html"

class UsuarioView (TemplateView):
    template_name = "paginas/index.html"

class CategoriaCreate(LoginRequiredMixin, CreateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome','descricao' ]
    success_url = reverse_lazy('index')
    extra_context={
        'titulo':' Cadastro de Categoria', 
        'botao': 'Cadastrar',
    }

class NoticiaCreate(LoginRequiredMixin, CreateView):
    model = Noticia
    fields = ['titulo','conteudo','postado_por','categoria']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-noticia')
    extra_context = {
        'titulo': 'Autentificar',
        'botao': 'Entrar',
    }

class ComentarioCreate(LoginRequiredMixin, CreateView):
    model = Comentario
    template_name = 'paginas/form.html'
    fields = ['noticia','conteudo']
    success_url = reverse_lazy('listar-comentario')
    extra_context = {
        'conteudo': 'Cadastrar Comentario',
        'botao': 'Cadastrar',
    }

class MidiaCreate(LoginRequiredMixin, CreateView):
    model = Midia 
    template_name = 'paginas/form.html'
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastrar Midia',
        'botao': 'Cadastrar',
   }
      
###############################################################

class CategoriaUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização de categoria',
        'botao' : 'Salvar',
    }

class NoticiaUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Noticia
    fields = ['titulo','conteudo','postado_por','categoria']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }

class ComentarioUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Comentario
    fields = ['noticia','conteudo']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }

class MidiaUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Midia 
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }


###################################################################


class ComentarioDelete(LoginRequiredMixin, DeleteView):
    model= Comentario 
    template_name='paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir - comentario',
        'botao' : 'Excluir',
    }


class NoticiaDelete(LoginRequiredMixin, DeleteView):
    model= Noticia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }
class CategoriaDelete(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index') 
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }

class MidiaDelete(LoginRequiredMixin, DeleteView):
    model= Midia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index') 
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }

####################################################################
class NoticiaList(LoginRequiredMixin, ListView):
    model = Noticia
    template_name = 'paginas/noticia.html'

class CategoriaList(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'paginas/categoria.html'

class MidiaList(LoginRequiredMixin, ListView):
    model = Midia
    template_name = 'paginas/midia.html'

class ComentarioList(LoginRequiredMixin, ListView):
    model = Comentario
    template_name = 'paginas/comentario.html'

####################################################################

class CategoriaUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Categoria
    template_name = 'paginas/categoria.html'

    fields = ['nome', 'descricao']

    success_url = reverse_lazy('index')

    success_message = "Categoria editada com sucesso!"

  
class CategoriaView(SuccessMessageMixin, CreateView):
    model = Categoria
    template_name = 'paginas/categoria.html'

    fields = ['nome', 'descricao']

    success_url = reverse_lazy('index')

    success_message = "Categoria criada com sucesso!"

class CategoriaDelete(SuccessMessageMixin, DeleteView):
    model = Categoria
    template_name = 'paginas/categoria.html'

    fields = ['nome', 'descricao']

    success_url = reverse_lazy('index')

    success_message = "Categoria deletada com sucesso!"






