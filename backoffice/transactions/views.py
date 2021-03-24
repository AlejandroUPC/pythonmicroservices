from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer
from django.shortcuts import render
from .forms import CreateNewSuperMarket
from .models import Transaction
from .serializers import TransactionSerializer, CustomerSerializer
from .producer import send_transaction

class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        transactions = Transaction.objects.all()
        serializer =  TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def create(self, request,customer_id):
        serializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_transaction(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, _id = None):
        transaction = Transaction.objects.get(id=_id)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    def remove(self, request, _id=None):
        transaction = Transaction.objects.get(id=_id)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomerAPIView(viewsets.ViewSet):
    def create_user(self, request, customer_id):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user(self,request,customer_id):
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


def createUser(response):
    form = CreateNewSuperMarket()
    return render(response, 'main/create.html',{"form":form})