from django.db import models

# Create your models here.
class Makale(models.Model):
    yazar = models.CharField(max_length=120)
    baslik = models.CharField(max_length=120)
    aciklama = models.CharField(max_length=200)
    metin = models.TextField()
    sehir = models.CharField(max_length=120)
    yayımlanma_tarihi = models.DateField()
    aktif = models.BooleanField(default=True)
    yaratilma_tarihi = models.DateTimeField(auto_now_add=True)
    güncelleneme_tarihi = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.baslik

