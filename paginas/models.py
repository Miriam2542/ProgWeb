from django.db import models
from django.contrib.auth.models import User


# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Categoria(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150, verbose_name="descrição")
    # cor was previously stored on Categoria but is now computed via template filter
    
    def __str__(self):
        return f"{self.nome}"
    class Meta:
        ordering = ['nome']
    
   
class Noticia(models.Model):
    # aumentar o limite para títulos mais longos (200 caracteres)
    titulo = models.CharField(max_length=200, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")  
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    # Indica se a notícia está publicada. Default True para manter comportamento atual.
    publicado = models.BooleanField(default=True, verbose_name="Publicada", help_text="Marque se a notícia está publicada e visível no site")
    imagem = models.ImageField(upload_to='noticias/', null=True, blank=True)
    data_publicacao = models.DateTimeField(auto_now_add=True, verbose_name="data de publicação" )
    postado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return f"{self.titulo}"
    class Meta:
        ordering = ['titulo']
    
class Comentario(models.Model):
    texto = models.CharField(max_length=250)
    data = models.DateTimeField(auto_now_add=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.PROTECT, verbose_name="Notícia")
    autor = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.autor} : {self.texto[:30]}"

    class Meta:
        # ordenar comentários do mais recente para o mais antigo
        ordering = ['-data']

class Midia(models.Model):
    titulo = models.CharField(max_length=150)
    url = models.URLField(max_length=250, blank=True, null=True, help_text="Link externo (opcional)")
    imagem = models.ImageField(upload_to='materias/images/', null=True, blank=True, verbose_name="Imagem")
    arquivo_pdf = models.FileField(upload_to='materias/pdfs/', null=True, blank=True, verbose_name="Arquivo PDF")
    descricao = models.CharField(max_length=200, verbose_name= "descrição", blank=True)
    fonte = models.CharField(max_length=150, blank=True)

    def __str__(self):
        # Mostra título e uma parte da descrição para identificação
        desc = (self.descricao[:50] + '...') if self.descricao and len(self.descricao) > 50 else (self.descricao or '')
        return f"{self.titulo} - {desc}"
    class Meta:
        ordering = ['titulo', 'descricao']
    


