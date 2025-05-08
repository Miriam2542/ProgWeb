from django.db import models

# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Categoria(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)
    descriação = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    

class Comentario (models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)


    def __str__(self):
        return self.name


class TipoSolicitacao(models.Model):
    descricao = models.CharField(max_length=250, verbose_name="descrição")
    nome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
