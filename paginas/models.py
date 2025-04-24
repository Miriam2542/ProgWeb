from django.db import models

# todas as classes DEVEM ter herança de models.Model
# Crie suas classes


class Campus(models.Model):
    # definir atributos
    nome = models.CharField(max_length=100)


class Curso (models.Model):
    nome = models.CharField(max_length=150)
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT)


class TipoSolicitacao(models.Model):
    descricao = models.CharField(max_length=250, verbose_name="descrição")
    nome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
    nome = models.CharField(max_length=100)
