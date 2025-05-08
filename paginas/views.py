from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, updateView, DeleteView
from.models import Campus, Curso

from django.urls import reverse_lazy
#importar a class Noticia
class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView (TemplateView):
 template_name = "paginas/sobre.html"

 class CampusCreate(CreateView):
    template_name = 'paginas/from.html'
    model = Campusfields= ['nome'] #lista com os nomes dos atributos
    success_url = reverse_lazy('inicio')
    extra_context={'título;'' Cadastro de Campus'}
    class CursoCreate(CreateView):
       template_name= 'paginas/from.html'