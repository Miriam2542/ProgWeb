from django.db import models
from django.contrib.auth.models import User


# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Categoria(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)
    descriação = models.CharField(max_length=150)
    
     def  __str__(self):
        return self.nome
    
   
class Noticia(models.Model):
     titulo = models.CharField(max_length=50)
     conteudo = models.TextField()  # Agora suporta texto grande
     categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
     data_publicacao = models.DateTimeField()
     postado_por = models.ForeignKey(User, on_delete=models.CASCADE)

     def __str__(self):
        return f"{self.titulo}"
    
class Comentario(models.Model):
    conteudo = models.CharField(max_length=250)
    data = models.DateTimeField()
    noticia = models.ForeignKey(Noticia, on_delete=models.PROTECT)

    def __str__(self):
        return f""

class Midia(models.Model):
     tipo = models.CharField(max_length=150)
     url = models.CharField(max_length=150)
     descricao = models.CharField(max_length=200, verbose_name= "descrição")
     fonte = models.CharField(max_length=150)

     def __str__(self):
        return f"{self.tipo} - {self.descricao}"


