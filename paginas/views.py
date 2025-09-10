from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia, User
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from braces.views import GroupRequiredMixin


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Listar as últimas três notícias
        context['ultimas_noticias'] = Noticia.objects.all().order_by('-data_publicacao')[:3]
        return context

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
        # Se for um superusuário (admin), pode editar qualquer notícia
        if self.request.user.is_superuser:
            obj = get_object_or_404(Noticia, pk=self.kwargs['pk'])
            return obj
        else:
            # Usuário normal só pode editar suas próprias notícias
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

    def get_object(self, queryset = None):
        obj = get_object_or_404(Comentario, pk=self.kwargs['pk'], autor=self.request.user) 
        return obj

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

    def get_object(self, queryset = None):
        obj = get_object_or_404(Comentario, pk=self.kwargs['pk'], autor=self.request.user) 
        return obj


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
    login_url = reverse_lazy('login')
    group_required = "Administrador"

    def get_queryset(self):
        # Se recebe o parâmetro "limite" na URL, filtra as notícias
        try:
            limite = int(self.request.GET.get('limite'))
        except (ValueError, TypeError):
            limite = None
        # COnsulta e ordana as notícias pela data de publicação decrescente
        noticias = Noticia.objects.all().order_by('-data_publicacao')

        # Se houver um limite, aplica o fatiamento de lista pela quantidade do limite
        if limite:
            noticias = noticias[:limite]
        return noticias

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
     
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Administrador').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ComentarioList(LoginRequiredMixin, ListView):
    model = Comentario
    template_name = 'paginas/comentario.html'

    def get_queryset(self):
        # Apenas comentários do usuário logado
        return Comentario.objects.filter(autor=self.request.user)
    

####################################################################

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'paginas/noticia_detalhe.html'
    context_object_name = 'noticia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtra os comentários relacionados à notícia atual
        context['comentarios'] = Comentario.objects.filter(noticia=self.object)
        return context