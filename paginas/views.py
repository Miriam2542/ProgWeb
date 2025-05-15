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
    template_name = 'paginas/from.html'
    model = Campusfields= ['nome','descricao' ]
    #lista com os nomes dos atributos
    success_url = reverse_lazy('inicio')
    extra_context={'título;'' Cadastro de Campus'}
    
    class NoticiaCreate(CreateView):
    template_name = 'paginas/from.html'
    model= conteudo 
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField()
    postado_por = models.ForeignKey(User, on_delete=models.CASCADE)

   

class Comentario(models.Model):
    conteudo = models.CharField(max_length=250)
    data = models.DateTimeField()
    noticia = models.ForeignKey(Noticia, on_delete=models.PROTECT)


class Midia(models.Model):
    tipo = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    descricao = models.CharField(max_length=200, verbose_name="descrição")
    fonte = models.CharField(max_length=150)

    class CursoCreate(CreateView):
       template_name= 'paginas/from.html'
       
       #######3##33#333
    class CategoriaUpdate(UpdateViewView):
     template_name = 'paginas/from.html'
    fields = ['nome']
    success_url = reverse_lazy('index')
    extra_context = {
        'título': 'Atualização'
        'botao' : 'Salvar',
    }