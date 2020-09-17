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