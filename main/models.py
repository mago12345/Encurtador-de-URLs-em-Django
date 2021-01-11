from django.db import models

class Link(models.Model):
    dest = models.CharField(max_length=2047) # url de destino
    alias = models.CharField(max_length=2047) # apelido da url
    total_views = models.IntegerField(default=0) # total de visualizações/cliques no link