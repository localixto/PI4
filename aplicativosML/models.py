from django.db import models

# Create your models here.
class Dados_Apontamentos(models.Model):

    data_envio=models.DateField()
    devedor=models.CharField(max_length=50)
    cpf_cnpj=models.CharField(max_length=18)
    especie=models.CharField(max_length=3)
    n_titulo=models.CharField(max_length=11)
    codigo_comarca=models.CharField(max_length=7)
    comarca=models.CharField(max_length=25)
    codigo_cartorio=models.CharField(max_length=2)
    nosso_numero=models.CharField(max_length=10)
    uf=models.CharField(max_length=2)
    cidade=models.CharField(max_length=25)
    valor_original=models.FloatField()
    valor_enviado=models.FloatField()
    status=models.CharField(max_length=25)


