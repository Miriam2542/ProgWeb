from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia

#importar a class Noticia
class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView (TemplateView):
    template_name = "paginas/sobre.html"

class CategoriaCreate(CreateView):
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome','descricao' ]
    success_url = reverse_lazy('inicio')
    extra_context={'título':' Cadastro de Categoria'}

class NoticiaCreate(CreateView):
    model = Noticia
    fields = ['categoria', 'data_publicacao']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('inicio')
    extra_context = {
        'titulo': 'Cadastrar Noticia',
        'botao': 'Cadastrar',
    }

class ComentarioCreate(CreateView):
    model = Comentario
    template_name = 'paginas/form.html'
    fields = ['noticia','conteudo']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'conteudo': 'Cadastrar Comentario',
        'botao': 'Cadastrar',
    }

class MidiaCreate(CreateView):
    model = Midia 
    template_name = 'paginas/form.html'
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'titulo': 'Cadastrar Midia',
        'botao': 'Cadastrar',
   }
      
###############################################################

class CategoriaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    fields = ['nome']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'título': 'Atualização',
        'botao' : 'Salvar',
    }

class NoticiaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    fields = ['nome']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'título': 'Atualização',
        'botao' : 'Salvar',
    }

class ComentarioUpdate(UpdateView):
    template_name = 'paginas/form.html'
    fields = ['nome']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'título': 'Atualização',
        'botao' : 'Salvar',
    }

class MidiaUpdate(UpdateView):
    template_name = 'paginas/form.html'
    fields = ['nome']
    success_url = reverse_lazy('inicio')
    extra_context = {
        'título': 'Atualização',
        'botao' : 'Salvar',
    }
class ComentarioDelete(DeleteView):
    model= Comentario 
    templete_name='cadastros/form-excluir.html'
    success_url = reverse_lazy('index')

class NoticiaDelete(DeleteView):
    model= Noticia
    templete_name='cadastros/form-excluir.html'
    success_url = reverse_lazy('index')

class CategoriaDelete(DeleteView):
    model= Categoria
    templete_name='cadastros/form-excluir.html'
    success_url = reverse_lazy('index')

class MidiaDelete(DeleteView):
    model= Midia
    templete_name='cadastros/form-excluir.html'
    success_url = reverse_lazy('index')


