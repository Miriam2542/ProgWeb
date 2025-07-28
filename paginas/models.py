from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User


# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Categoria(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.nome}"
    
   
class Noticia(models.Model):
    titulo = models.CharField(max_length=50)
    conteudo = models.TextField()  
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    data_publicacao = models.DateTimeField(auto_now_add=True)
    postado_por = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.titulo}"
    
class Comentario(models.Model):
    nome = models.CharField(max_length=100)
    conteudo = models.CharField(max_length=250)
    data = models.DateTimeField(auto_now_add=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome} ({self.conteudo})"

class Midia(models.Model):
    tipo = models.CharField(max_length=150)
    url = models.URLField(max_length=150)
    descricao = models.CharField(max_length=200, verbose_name= "descricao")
    fonte = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.tipo} - {self.descricao}"


