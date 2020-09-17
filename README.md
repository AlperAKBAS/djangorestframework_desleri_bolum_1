# Django RestFramework Dersleri - Bölüm 1
BU DİZİN YOUTUBE DERSLERİ İÇİN YARATILMIŞTIR.
VİDEO TUTORIAL SERİSİ İÇİN LİNK:  [Django RestFramework Dersleri - Bölüm 1 - YouTube](https://www.youtube.com/playlist?list=PLtf2C1UGjgPBgBLXvS61dDYJodJ4qhBRi)

## Açıklama:
En çok kullanılan ve en güçlü Python Web Framework'ü olan Django’da, RestFrameWork kütüphanesini öğreniyoruz. Böylelikle, Django'nun gücünü kullanarak, rest api akışları yaratabileceğiz. Bu ders serisinin sonunda, hem Django RestFrameWork konusunda sağlam bir temeliniz oluşacak; hem de listeleme, yaratma, güncelleme ve silme işlemlerini rahatlıkla yapabilecek ve hatta veri doğrulama yapabilecek seviyeye geleceksiniz. Bu serinin devamı niteliğinde iki adet daha video serimiz olacak. Bu serilerde de Django RestFrameWork  konusunda çok daha ileri seviye bilgiler edineceğiz.

## Neden RestFrameWork?
Sıradan bir web framework ile bir çok işlem gerçekleştirebiliriz Ancak, browserlar ile sınırlı kalırız. Ancak, uygulama backendimizi rest api beslemeleri şeklinde yaparsak ,tek bir sunucudan, hem web sayfaları (dinamik), hem mobil aplikasyonlar yaratabiliriz. Bunun yanında, API akışlarımız olacağından, internete bağlı çalışan herhangi bir uygulama ile backendimiz arasında rahatlıkla iletişim kurabiliriz. 

Normal Django versiyonunda,  backendimizi yaratırken, frontend ile de uğraşmak durumundayız. Çünkü, yarattığımız model ve viewleri eş zamanlı olarak kontrol de etmeliyiz. 

Ancak Django RestFramework ile, hali hazırda bir borwsable api yapısı geldiğinden, geliştiriciler için gerekli tüm html yapıları da birlikte geliyor. Bu da demek oluyor ki,  çok daha kısa bir sürede çok daha hızlı yol alabiliriz.

## Peki Bu seride neleri göreceğiz?
1. Giriş / Gerekli kurulumlar ve Django Projemizin ayağa kaldırılması
2. Serializers nedir? Önemi? serializers.Serializer ile ilk serlializerımızın oluşturulması.
3. İkinci videomuzun devamı. Django Shell (shell_plus) ile serialize ve deserialize işlemlerinin yapılması
4. @api_view dekoratörümüz ile ilk view ve end pointumuzun (url) yaratılması - Function Based Views [list_create_api_view(request)]
5.  @api_view dekoratörümüz ile ikinci view ve end pointumuzun (url) yaratılması - Function Based Views [detail_api_view(request)]
6. Class Based Viewlere Giriş - APIView classıyla, ListCreate ve DetailAPI viewlerin yaratılması
7. Veri Doğrulama (Validation) - Kendi Veri Doğrulama sistemlerimizin Serializerımıza entegre edilmesi
8. ModelSerializer - kod yükünden kurtulmaya başlıyoruz.
9. Nested Relationships - Modeller arasındaki ilişkileri nasıl yöneteceğiz - giriş seviyesi.

- - - -

## KOD SNIPPETLER VE AÇILAMALAR
### 1. Proje sonundaki dizinimiz
```terminal
.
├── db.sqlite3
├── haberbulteni
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── haberler
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── manage.py
```

### 2. Modeller
2.1 İlk hali - haberler/models.py 
```python
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

```

2.2 Son hali - haberler/models.py 
```python
from django.db import models

# Create your models here.
class Gazeteci(models.Model):
    isim = models.CharField(max_length=120)
    soyisim = models.CharField(max_length=120)
    biyografi = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.isim} {self.soyisim}'


class Makale(models.Model):
    yazar = models.ForeignKey(Gazeteci, on_delete=models.CASCADE, related_name='makaleler')
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

```



### 3. İlk Serializerımız - 2 ve 3. Videolar

haberler/api/serializers_ilk.py
```python
from rest_framework import serializers
from haberler.models import Makale, Gazeteci


#### STANDART SERIALIZER
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayımlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncelleneme_tarihi  = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayımlanma_tarihi = validated_data.get('yayımlanma_tarihi', instance.yayımlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance

    def validate(self, data): # object level
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Baslik ve açıklama alanları aynı olamaz. Lütfen farklı bir açıklama giriniz.')
        return data

    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Baslik alani minimum 20 karakter olmalı. siz {len(value)} karakter girdiniz.')
        return value

```


### 4. Proje Sonu İtibariyle Serializerlarımız
haberler/api/serializers.py
```python
from rest_framework import serializers
from haberler.models import Makale, Gazeteci


from datetime import datetime
from datetime import date
from django.utils.timesince import timesince



class MakaleSerializer(serializers.ModelSerializer):

    time_since_pub = serializers.SerializerMethodField()
    # yazar = serializers.StringRelatedField()

    class Meta:
        model = Makale
        fields = '__all__'
        # fields = ['yazar', 'baslik', 'metin']
        # exclude = ['yazar', 'baslik', 'metin']
        read_only_fields = ['id', 'yaratilma_tarihi', 'güncelleneme_tarihi']

    def get_time_since_pub(self,object):
        now = datetime.now()
        pub_date = object.yayımlanma_tarihi
        if object.aktif == True:
            time_delta = timesince(pub_date, now)
            return time_delta
        else:
            return 'Aktif Degil!'

    def validate_yayımlanma_tarihi(self, tarihdegeri):
        today = date.today()
        if tarihdegeri > today:
            raise serializers.ValidationError('Yayımlanma tarihi ileri bir tarih olamaz!')
        return tarihdegeri



class GazeteciSerializer(serializers.ModelSerializer):

    # makaleler = MakaleSerializer(many=True, read_only=True)
    makaleler = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='makale-detay',
    )

    class Meta:
        model = Gazeteci
        fields = '__all__'


```


### 5.  Function Based Views — @api_view dekoratörü ile
haberler/api/views_ilk.py
```python
from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

from haberler.models import Makale
from haberler.api.serializers import MakaleSerializer



@api_view(['GET', 'PUT', 'DELETE'])
def makale_detail_api_view(request, pk):
    try:
        makale_instance = Makale.objects.get(pk=pk)
    except Makale.DoesNotExist:
        return Response(
            {
                'errors': {
                    'code': 404,
                    'message': f'Böyle bir id ({pk}) ile ilgili makale bulunamadı.'
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = MakaleSerializer(makale_instance) 
        return Response(serializer.data)


    elif request.method == 'PUT':
        serializer = MakaleSerializer(makale_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'DELETE':
        makale_instance.delete()
        return Response(
            {
                'işlem': {
                    'code': 204,
                    'message': f'({pk}) id numaralı makale silinmiştir.'
                }
            },
            status = status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def makale_list_create_api_view(request):
    
    if request.method == 'GET':
        makaleler = Makale.objects.filter(aktif=True) 
        serializer = MakaleSerializer(makaleler, many=True) 
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
```

Function views için url endpointlerimiz
haberler/api/urls.py
```python

from django.urls import path
from haberler.api import views as api_views

urlpatterns = [
    path('makaleler/',api_views.makale_list_create_api_view, name='makale-listesi'),
    path('makaleler/<int:pk>', api_views.makale_detail_api_view, name='makale-detay'),
]

```

### 6.  APIViewlerimiz
haberler/api/views.py
```python
from rest_framework import status
from rest_framework.response import Response 
# from rest_framework.decorators import api_view

from haberler.models import Makale, Gazeteci
from haberler.api.serializers import MakaleSerializer, GazeteciSerializer

#class views
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404



class GazeteciListCreateAPIView(APIView):
    def get(self, request):
        yazarlar = Gazeteci.objects.all()
        serializer = GazeteciSerializer(yazarlar, many=True, context={'request': request}) 
        return Response(serializer.data)


    def post(self, request):
        serializer = GazeteciSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MakaleListCreateAPIView(APIView):
    def get(self, request):
        makaleler = Makale.objects.filter(aktif=True) 
        serializer = MakaleSerializer(makaleler, many=True) 
        return Response(serializer.data)


    def post(self, request):
        serializer = MakaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakaleDetailAPIView(APIView):

    def get_object(self, pk):
        makale_instance = get_object_or_404(Makale, pk=pk)
        return makale_instance

    def get(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale) 
        return Response(serializer.data)       

    def put(self, request, pk):
        makale = self.get_object(pk=pk)
        serializer = MakaleSerializer(makale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

    def delete(self, request, pk):
        makale = self.get_object(pk=pk)
        makale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

```

APIViews için url endpointlerimiz
haberler/api/urls.py
```python
from django.urls import path
from haberler.api import views as api_views

urlpatterns = [
    path('yazarlar/',api_views.GazeteciListCreateAPIView.as_view(), name='yazar-listesi'),
    path('makaleler/',api_views.MakaleListCreateAPIView.as_view(), name='makale-listesi'),
    path('makaleler/<int:pk>', api_views.MakaleDetailAPIView.as_view(), name='makale-detay'),
]
```

### 6.  Settings.py ‘INSTALLED_APPS’
haberbulteni/settings.py
```python
#
#
# 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'haberler.apps.HaberlerConfig',
]

#
#
```

- - - -

VİDEO TUTORIAL SERİSİ İÇİN LİNK:  [Django RestFramework Dersleri - Bölüm 1 - YouTube](https://www.youtube.com/playlist?list=PLtf2C1UGjgPBgBLXvS61dDYJodJ4qhBRi)



# djangorestframework_desleri_bolum_1
# djangorestframework_desleri_bolum_1
