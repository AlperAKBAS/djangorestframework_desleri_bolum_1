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



