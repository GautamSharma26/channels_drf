from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializer import *
from .models import *
from .permission import IsOwner
from rest_framework.response import Response


class PizzaAdminView(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()

    def destroy(self, request, *args, **kwargs):
        super(PizzaAdminView, self).destroy(request, *args, **kwargs)
        return Response({'message': 'Pizza Deleted'})

    def partial_update(self, request, *args, **kwargs):
        super(PizzaAdminView, self).partial_update(request, *args, **kwargs)
        return Response({'message': 'Product updated successfully'})


class PizzaAllView(viewsets.ModelViewSet):
    serializer_class = PizzaSerializer
    queryset = Pizza.objects.all()


class AddressView(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    serializer_class = AddressSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        queryset = Address.objects.filter(user=user)
        return queryset


class AddressWrite(viewsets.ModelViewSet):
    permission_classes = [IsOwner, IsAuthenticated]
    serializer_class = AddressWriteSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        super(AddressWrite, self).destroy(request, *args, **kwargs)
        return Response({'message': 'Address Deleted'})

    def partial_update(self, request, *args, **kwargs):
        super(AddressWrite, self).partial_update(request, *args, **kwargs)
        return Response({'message': 'Address updated'})


class AddressCreate(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressWriteSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': f'Address created for {user.first_name}'})
        return Response({'error': serializer.errors})

