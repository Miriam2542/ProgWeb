from django.views.generic import TemplateView

class Inicio(TemplateView):
    template_name = "paginas/index.html"

class SobreView (TemplateView):
 template_name = "paginas/sobre.html"