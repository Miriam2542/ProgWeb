from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Categoria, Noticia, Comentario, Midia
from django.db.models.deletion import ProtectedError
from django.db import transaction
from django.contrib.auth.models import User, Group
from .forms import UsuarioCadastroForm
from django.shortcuts import get_object_or_404
from braces.views import GroupRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import redirect


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
        # Listar as últimas três notícias (somente publicadas quando o campo existir)
        if hasattr(Noticia, 'publicado'):
            context['ultimas_noticias'] = Noticia.objects.filter(publicado=True).order_by('-data_publicacao')[:3]
        else:
            context['ultimas_noticias'] = Noticia.objects.all().order_by('-data_publicacao')[:3]
        return context

class SobreView (TemplateView):
    template_name = "paginas/sobre.html"

class UsuarioView (TemplateView):
    template_name = "paginas/index.html"

class CategoriaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome','descricao']
    success_url = reverse_lazy('index')
    extra_context={
        'titulo':' Cadastro de Categoria', 
        'botao': 'Cadastrar',
    }

class NoticiaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    model = Noticia
    fields = ['titulo','conteudo','categoria','imagem']
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
    fields = ['titulo', 'url', 'imagem', 'arquivo_pdf', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Cadastrar Matéria Complementar',
        'botao': 'Cadastrar',
   }
   
      
###############################################################

class CategoriaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    template_name = 'paginas/form.html'
    model = Categoria
    fields = ['nome', 'descricao']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização de categoria',
        'botao' : 'Salvar',
    }

class NoticiaUpdate(LoginRequiredMixin, UpdateView):
    # Permite que o autor da notícia (postado_por) ou superusuário edite.
    login_url = reverse_lazy('login')
    template_name = 'paginas/form.html'
    model = Noticia
    fields = ['titulo','conteudo','postado_por','categoria','imagem']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização',
        'botao' : 'Salvar',
    }

    def get_object(self, queryset = None):
        # Se for um superusuário (admin) ou membro do grupo 'Admin', pode editar qualquer notícia
        user = self.request.user
        is_admin_group = user.groups.filter(name='Admin').exists()
        if user.is_superuser or is_admin_group:
            obj = get_object_or_404(Noticia, pk=self.kwargs['pk'])
            return obj
        # Usuário normal só pode editar suas próprias notícias
        obj = get_object_or_404(Noticia, pk=self.kwargs['pk'], postado_por=user)
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
        # Allow superuser or members of 'Admin' group to edit any comment,
        # otherwise only the comment author can edit.
        user = self.request.user
        is_admin_group = user.groups.filter(name='Admin').exists()
        if user.is_superuser or is_admin_group:
            obj = get_object_or_404(Comentario, pk=self.kwargs['pk'])
            return obj
        obj = get_object_or_404(Comentario, pk=self.kwargs['pk'], autor=user)
        return obj

class MidiaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    # Apenas membros do grupo 'Admin' (ou superuser) podem editar matérias complementares
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    template_name = 'paginas/form.html'
    model = Midia 
    fields = ['titulo', 'url', 'imagem', 'arquivo_pdf', 'descricao', 'fonte']
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Atualização de Matéria Complementar',
        'botao' : 'Salvar',
    }


###################################################################


class ComentarioDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    model = Comentario
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir - comentário',
        'botao': 'Excluir',
    }

    def get_object(self, queryset=None):
        # Somente administradores podem excluir comentários
        obj = get_object_or_404(Comentario, pk=self.kwargs['pk'])
        return obj


class NoticiaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    model= Noticia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir',
        'botao' : 'Excluir',
    }
    def get_object(self, queryset=None):
        # Apenas administradores podem excluir notícias
        obj = get_object_or_404(Noticia, pk=self.kwargs['pk'])
        return obj

    def delete(self, request, *args, **kwargs):
        # Ao excluir uma Notícia, remover comentários relacionados primeiro para evitar
        # ProtectedError (sintonia com comportamento esperado de remoção em cascata).
        obj = self.get_object()
        # import local to avoid circular imports at module load time (safety)
        from .models import Comentario

        # Tenta remover comentários associados antes de excluir a notícia.
        # Usa uma transação para garantir consistência.
        with transaction.atomic():
            Comentario.objects.filter(noticia=obj).delete()
            try:
                return super().delete(request, *args, **kwargs)
            except ProtectedError:
                # Em casos raros de concorrência ou relacionamentos adicionais,
                # tenta apagar comentários novamente e refaz a operação.
                Comentario.objects.filter(noticia=obj).delete()
                return super().delete(request, *args, **kwargs)
    
class CategoriaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    # Apenas membros do grupo 'Admin' (ou superuser) podem excluir categorias
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    model = Categoria
    template_name = 'paginas/form.html'
    success_url = reverse_lazy('index')
    extra_context = {
        'titulo': 'Excluir',
        'botao': 'Excluir',
    }

    def delete(self, request, *args, **kwargs):
        """Tenta excluir a Categoria; se houver objetos protegidos (Noticia), captura
        ProtectedError e informa o usuário com uma mensagem amigável em vez de retornar
        um trace de erro."""
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Não é possível excluir esta categoria porque existem notícias associadas. Remova ou reatribua as notícias antes de excluir a categoria.')
            return redirect('listar-categoria')


class CategoriaConfirmDeleteView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    """Página de confirmação mais amigável para exclusão de Categoria.
    Mostra as notícias relacionadas e permite:
      - reatribuir as notícias para outra categoria,
      - apagar as notícias relacionadas (apaga comentários antes),
      - cancelar.

    Só membros do grupo 'Admin' (ou superuser) podem acessar.
    """
    template_name = 'paginas/categoria_confirm_delete.html'
    login_url = reverse_lazy('login')
    group_required = ["Admin"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        categoria = get_object_or_404(Categoria, pk=pk)
        # Se o modelo Noticia possui um campo que indica publicação (ex: 'publicado' ou 'status'),
        # apenas consideramos notícias publicadas para reatribuição/exclusão em massa.
        # Usamos hasattr para manter compatibilidade sem exigir migrações.
        if hasattr(Noticia, 'publicado'):
            noticias = Noticia.objects.filter(categoria=categoria, publicado=True)
            filtrando_publicadas = True
        else:
            noticias = Noticia.objects.filter(categoria=categoria)
            filtrando_publicadas = False
        outras_categorias = Categoria.objects.exclude(pk=categoria.pk)
        context.update({
            'categoria': categoria,
            'noticias_relacionadas': noticias,
            'filtrando_publicadas': filtrando_publicadas,
            'outras_categorias': outras_categorias,
        })
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        categoria = get_object_or_404(Categoria, pk=pk)

        action = request.POST.get('action')

        if action == 'cancel':
            messages.info(request, 'Operação de exclusão cancelada.')
            return redirect('listar-categoria')

        # Reatribuir: receber id da nova categoria
        if action == 'reassign':
            try:
                nova_pk = int(request.POST.get('new_category'))
                nova_cat = get_object_or_404(Categoria, pk=nova_pk)
            except (TypeError, ValueError):
                messages.error(request, 'Categoria de destino inválida.')
                return redirect('excluir-categoria', pk=pk)
            # Reatribui apenas as notícias consideradas no contexto (p.ex. apenas publicadas)
            if hasattr(Noticia, 'publicado'):
                noticias_para_mover = Noticia.objects.filter(categoria=categoria, publicado=True)
            else:
                noticias_para_mover = Noticia.objects.filter(categoria=categoria)

            with transaction.atomic():
                noticias_para_mover.update(categoria=nova_cat)
                # Se ainda existirem notícias (não-publicadas), a categoria pode permanecer protegida;
                # tentamos excluir e capturamos ProtectedError mais acima na lógica padrão.
                try:
                    categoria.delete()
                except ProtectedError:
                    messages.warning(request, 'A categoria foi reatribuída para as notícias publicadas, mas existem notícias não-publicadas que impedem a exclusão. Reavalie antes de excluir.')
                    return redirect('listar-categoria')
            messages.success(request, 'Categoria excluída e notícias reatribuídas com sucesso.')
            return redirect('listar-categoria')

        # Apagar notícias relacionadas (apaga comentários primeiro)
        if action == 'delete_notices':
            # Deletar apenas as notícias consideradas (p.ex. apenas publicadas) e seus comentários
            if hasattr(Noticia, 'publicado'):
                noticias_para_apagar = Noticia.objects.filter(categoria=categoria, publicado=True)
            else:
                noticias_para_apagar = Noticia.objects.filter(categoria=categoria)

            with transaction.atomic():
                from .models import Comentario
                Comentario.objects.filter(noticia__in=noticias_para_apagar).delete()
                noticias_para_apagar.delete()
                # Tenta excluir a categoria; se ainda existirem notícias (não-publicadas), a exclusão pode falhar e será tratada
                try:
                    categoria.delete()
                except ProtectedError:
                    messages.warning(request, 'As notícias publicadas foram removidas, mas existem notícias não-publicadas que impedem a exclusão da categoria.')
                    return redirect('listar-categoria')
            messages.success(request, 'Categoria e notícias relacionadas foram removidas com sucesso.')
            return redirect('listar-categoria')

        # Caso não reconheça a ação
        messages.error(request, 'Ação inválida.')
        return redirect('listar-categoria')

class MidiaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    # Apenas membros do grupo 'Admin' (ou superuser) podem excluir matérias complementares
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
    model= Midia
    template_name ='paginas/form.html'
    success_url = reverse_lazy('index') 
    extra_context = {
        'titulo': 'Excluir - Matéria Complementar',
        'botao' : 'Excluir',
    }

####################################################################
class NoticiaList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = ["Admin"]
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
        # Exibir somente notícias publicadas no list view público, quando disponível
        if hasattr(Noticia, 'publicado'):
            noticias = Noticia.objects.filter(publicado=True).order_by('-data_publicacao')
        else:
            noticias = Noticia.objects.all().order_by('-data_publicacao')

        # Filtra por categoria quando ?categoria=<pk> for passado na URL
        try:
            categoria_pk = self.request.GET.get('categoria')
            if categoria_pk:
                categoria_pk = int(categoria_pk)
                noticias = noticias.filter(categoria__pk=categoria_pk)
        except (ValueError, TypeError):
            # Ignora filtros inválidos
            pass

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
    
    # Se quiser restringir a visualização a administradores, descomente o método abaixo
    # e ajuste o nome do grupo conforme usado no sistema ('Admin' ou 'Administrador').
    # Atualmente deixamos aberto para que todos os usuários logados vejam as mídias.
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.groups.filter(name='Admin').exists():
    #         raise PermissionDenied
    #     return super().dispatch(request, *args, **kwargs)

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
        # Formulário de comentário para o template (apenas renderizado, validação via POST)
        from .forms import ComentarioForm
        context['comentario_form'] = ComentarioForm()
        return context

    def post(self, request, *args, **kwargs):
        # Trata submissão do formulário de comentário vindo do template
        # Garante que o usuário esteja autenticado (padrão: LoginRequired em outro lugar)
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa estar logado para comentar.')
            return redirect('detalhar-noticia', pk=self.get_object().pk)

        from .forms import ComentarioForm
        form = ComentarioForm(request.POST)
        noticia = self.get_object()
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.noticia = noticia
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso.')
            return redirect('detalhar-noticia', pk=noticia.pk)
        else:
            # Se inválido, renderiza a página com erros
            context = self.get_context_data()
            context['comentario_form'] = form
            return self.render_to_response(context)


@login_required
def limpar_comentarios(request, pk):
    """Apaga todos os comentários associados a uma notícia.

    Acesso restrito a superusers ou membros do grupo 'Admin'.
    Executa via POST (form com CSRF) e redireciona para a página de detalhe.
    """
    # Verifica permissão
    if not (request.user.is_superuser or request.user.groups.filter(name='Admin').exists()):
        messages.error(request, 'Permissão negada.')
        return redirect('detalhar-noticia', pk=pk)

    noticia = get_object_or_404(Noticia, pk=pk)
    # Deleta comentários relacionados
    Comentario.objects.filter(noticia=noticia).delete()
    messages.success(request, 'Todos os comentários foram removidos desta notícia.')
    return redirect('detalhar-noticia', pk=pk)