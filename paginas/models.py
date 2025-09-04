from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User


# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Categoria(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150, verbose_name="descrição")
    
    def __str__(self):
        return f"{self.nome}"
class Meta: 
        ordering = ['nome']
    
   
class Noticia(models.Model):
    titulo = models.CharField(max_length=50, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")  
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
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
        ordering = ['-autor']

class Midia(models.Model):
    tipo = models.CharField(max_length=150)
    url = models.URLField(max_length=150)
    descricao = models.CharField(max_length=200, verbose_name= "descrição")
    fonte = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.tipo} - {self.descricao}"
class Meta: 
    ordering = ['tipo', 'descricao']
    


