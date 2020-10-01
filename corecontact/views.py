from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PeopleSerializer, ContactSerializer
from .models import People, Contacts
from rest_framework import status


class PeopleAPIView(APIView):
    def post(self, request):
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)


class ContactAPIView(APIView):
    def get(self, request):
        number = request.GET.get('number', None)
        email = request.GET.get('email', None)
        name = request.GET.get('name', None)

        contactlist = \
            Contacts.objects.textsearchemailnum(email, number)
        peoplelist = People.objects.textsearch(name)
        peoplepk = list()
        if contactlist is not None:
            for contact in contactlist:
                peoplepk.append(contact.people.pk)
        for people in peoplelist:
            peoplepk.append(people.pk)
        peoplepk = list(dict.fromkeys(peoplepk))
        listofpeople = People.objects.filter(pk__in=peoplepk)
        serializer = PeopleSerializer(listofpeople, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        try:
            people = People.objects.get(pk=id)
        except People.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request.data['people'] = id
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)
