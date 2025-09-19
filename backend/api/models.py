from django.db import models

# Create your models here.

class Tarefa(models.Model): 
    STATUS_CHOICE = [
        ('PENDENTE', 'Pendente'),
        ('ANDAMENTO', 'Em andamento'),
        ('FINALIZADA', 'Finalizada')
    ]

    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta')
    ]
    
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data_inicio = models.DateField()
    data_termino = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default="PENDENTE"
        )
    prioridade = models.CharField(
        max_length=20,
        choices=PRIORIDADE_CHOICES,
        default="MEDIA"
    )
    responsavel = models.CharField(max_length= 100, blank=True, null=True)
    observacoes = models.TextField( blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} - {self.status} - {self.prioridade}"
