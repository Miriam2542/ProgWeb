from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia, User
from django.views.generic import TemplateView , ListView
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django.shortcuts import get_object_or_404



# Crie a view no final do arquivo ou em outro local que faça sentido


class CadastroUsuarioView(CreateView):
    model = User
    # Não tem o fields, pois ele é definido no forms.py
    form_class = UsuarioCadastroForm
    # Pode utilizar o seu form padrão
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('login')
    extra_context ={
        'titulo': 'Cadastro de Usuário',
        'botao': 'Cadastrar',
    } 



    def form_valid(self, form):
        # Faz o comportamento padrão do form_valid
        url = super().form_valid(form)
        # Busca ou cria um grupo com esse nome
        grupo, criado = Group.objects.get_or_create(name='Usuário')
        # Acessa o objeto criado e adiciona o usuário no grupo acima
        self.object.groups.add(grupo)
        # Retorna a URL de sucesso
        return url

 

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
    fields = ['titulo','conteudo','categoria']
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('listar-noticia')
    extra_context = {
        'titulo': 'Cadastro de Notícia',
        'botao': 'Entrar',
    }

    def form_valid(self, form):
        #pegar usuario que está autentificado
       form.instance.postado_por = self.request.user
       url=super().form_valid(form)
       return url
    

class ComentarioCreate(LoginRequiredMixin, CreateView):
    model = Comentario
    template_name = 'paginas/form.html'
    fields = ['noticia','texto']
    success_url = reverse_lazy('listar-comentario')
    extra_context = {
        'titulo': 'Cadastrar Comentário',
        'botao': 'Cadastrar',
    }
    def form_valid(self, form):
       #pegar usuario que está autentificado
       form.instance.autor = self.request.user
       url=super().form_valid(form)
       return url

class MidiaCreate(LoginRequiredMixin, CreateView):
    model = Midia 
    template_name = 'paginas/form.html'
    fields = ['tipo', 'url', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastrar Mídia',
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

    def get_object(self, queryset = None):
        
        obj = get_object_or_404(Noticia, pk=self.kwargs['pk'], postado_por=self.request.user) 
        return obj

class ComentarioUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'paginas/form.html'
    model = Comentario
    fields = ['noticia','texto']
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
    def get_object(self, queryset = None):
        
        obj = get_object_or_404(Noticia, pk=self.kwargs['pk'], postado_por=self.request.user) 
        return obj
    
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

# fazer herança para ter tudo que tem na NoticiaList
class MinhasNoticias(NoticiaList):

    def get_queryset(self):
        qs = Noticia.objects.filter(postado_por=self.request.user)
        return qs

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






