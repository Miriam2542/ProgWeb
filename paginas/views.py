
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia
from django.views.generic import TemplateView , ListView
 
#importar a class Noticia
class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView (TemplateView):
    template_name = "paginas/sobre.html"

class CategoriaCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome','descricao' ]
    success_url = reverse_lazy('index')
    extra_context={
        'titulo':' Cadastro de Categoria', 
        'botao': 'Cadastrar',
    }

class NoticiaCreate(CreateView):
    model = Noticia
    fields = ['titulo','conteudo','postado_por','categoria']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastrar Noticia',
        'botao': 'Cadastrar',
    }

class ComentarioCreate(CreateView):
    model = Comentario
    template_name = 'paginas/form.html'
    fields = ['noticia','conteudo']
    success_url = reverse_lazy('index')
    extra_context = {
        'conteudo': 'Cadastrar Comentario',
        'botao': 'Cadastrar',
    }

class MidiaCreate(CreateView):
    model = Midia 
    template_name = 'paginas/form.html'
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastrar Midia',
        'botao': 'Cadastrar',
   }
      
###############################################################

class CategoriaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização de categoria',
        'botao' : 'Salvar',
    }

class NoticiaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Noticia
    fields = ['titulo','conteudo','postado_por','categoria']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }

class ComentarioUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Comentario
    fields = ['noticia','conteudo']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }

class MidiaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    model = Midia 
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }


###################################################################


class ComentarioDelete(DeleteView):
    model= Comentario 
    template_name='paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir - comentario',
        'botao' : 'Excluir',
    }


class NoticiaDelete(DeleteView):
    model= Noticia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }
class CategoriaDelete(DeleteView):
    model = Categoria
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index') 
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }

class MidiaDelete(DeleteView):
    model= Midia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index') 
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }

####################################################################
class NoticiaList(ListView):
    model = Noticia
    template_name = 'paginas/noticia.html'

class CategoriaList(ListView):
    model = Categoria
    template_name = 'paginas/categoria.html'

class MidiaList(ListView):
    model = Midia
    template_name = 'paginas/midia.html'

class ComentarioList(ListView):
    model = Comentario
    template_name = 'paginas/comentario.html'


