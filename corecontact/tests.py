from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework.test import APIClient
import json


class PoepleTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.restapiClient = APIClient()

    def test_peoplePost(self):
        response = \
            self.restapiClient.post(
                reverse_lazy('peopleview'),
                data={
                    'name': 'Ultron',
                    'age': 29,
                    'height': 155},
                format='json')
        assert response.status_code == 201
        peoplejson = json.loads(response.content)
        assert peoplejson['name'] == 'Ultron'

        response = \
            self.restapiClient.post(
                reverse_lazy('insertcontactpeople', kwargs={
                    'id': 1}
                ),
                data={
                    'email': 'ultron@avengers.com',
                    'number': '0198345212'},
                format='json')
        assert response.status_code == 201
        contactpeoplejson = json.loads(response.content)
        assert contactpeoplejson['email'] == 'ultron@avengers.com'
        assert contactpeoplejson['people'] == 1

        response = \
            self.restapiClient.post(
                reverse_lazy('insertcontactpeople', kwargs={
                    'id': 2}
                ),
                data={
                    'email': 'ultron@avengers.com',
                    'number': '0198345212'},
                format='json')
        assert response.status_code == 500


class SearchTextTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.restapiClient = APIClient()

        self.restapiClient.post(
            reverse_lazy('peopleview'),
            data={
                'name': 'Ultron',
                'age': 29,
                'height': 155},
            format='json')

        self.restapiClient.post(
            reverse_lazy('peopleview'),
            data={
                'name': 'Notron',
                'age': 40,
                'height': 100},
            format='json')

        self.restapiClient.post(
                reverse_lazy('insertcontactpeople', kwargs={
                    'id': 1}
                ),
                data={
                    'email': 'ultron@avengers.com',
                    'number': '0198345212'},
                format='json')
    
    def url_builder(self, reversename, querystring):
        url = '{baseurl}?{querystring}'.format(
            baseurl=reverse_lazy(reversename),
            querystring=querystring
        )
        return url

    def test_searchTextPeopleOnly(self):
        url = self.url_builder('contactsearch', 'name=Notron')

        response = self.restapiClient.get(
                url,
                format='json')
        # print (response)
        assert response.status_code == 200
        searchTextJson = json.loads(response.content)
        assert searchTextJson[0]['name'] == 'Notron'
    
    def test_searchTextNameEmail(self):
        url = self.url_builder('contactsearch', 'name=Notron&email=ultron@')

        response = self.restapiClient.get(
                url,
                format='json')
        # print (response)
        assert response.status_code == 200
        searchTextJson = json.loads(response.content)
        assert searchTextJson[0]['name'] == 'Ultron'
        assert searchTextJson[1]['name'] == 'Notron'


    def test_searchTextNameEmailPhone(self):
        url = self.url_builder(
            'contactsearch', 
            'name=Notron&email=nosuchperson@&number=0198345212')

        response = self.restapiClient.get(
                url,
                format='json')
        # print (response)
        assert response.status_code == 200
        searchTextJson = json.loads(response.content)
        assert searchTextJson[0]['name'] == 'Ultron'
        assert searchTextJson[1]['name'] == 'Notron'
