from omok.models import Room
from toy_auth.models import GuestUser
from django.test.client import RequestFactory
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase
from toy_auth.middleware import passTokenTest
import os

class TestUserSchema(TestCase):
    def setUp(self):
        self.client = Client(schema, middleware=[passTokenTest])
        self.request = RequestFactory().get('/')
        self.user = GuestUser.objects.signIn(token='')
        self.uid = self.user.id
        self.rid = Room.objects.create(title='test',
                                    password='1234',
                                    isAvailable=True,
                                    hasPassword=True,
                                    user=self.user).pk

    def test_create_room(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            mutation ($title:String, $password:String)
            {
                createRoom(title:$title, password:$password) {
                    id
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'title': 'I am testing'},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('createRoom').get('id') is not None
    
    def test_query_rooms(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            query 
            {
                rooms {
                    id
                    title
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('rooms') is not None 


    def test_query_room(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            query ($id:ID, $password:String)
            {
                room(id:$id, password:$password) {
                    id
                    title
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'id': self.rid, 'password': '1234'},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('room').get('id') == str(self.rid)

    def test_update_room(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid

        query = """
            mutation ($id:ID, $title:String, $password:String, $isAvailable:Boolean)
            {
                updateRoom(id:$id, title:$title, password:$password, isAvailable:$isAvailable) {
                    id
                    title
                    hasPassword
                    isAvailable
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'id': self.rid, 'title': 'I am testing', 'isAvailable': False},
            context_value = self.request
        )

        assert response.get('data').get('updateRoom').get('title') == 'I am testing' 
        assert response.get('data').get('updateRoom').get('hasPassword') == False
        assert response.get('data').get('updateRoom').get('isAvailable') == False


    def test_delete_room(self):
        self.request.uid = self.uid
        self.request.adminKey = os.environ['SECRET_KEY']

        query = """
            mutation ($id:ID)
            {
                deleteRoom(id:$id) {
                    id
                }
            }
        """
        response = self.client.execute(
            query,
            variables = {'id': self.rid},
            context_value = self.request
        )

        assert 'errors' not in response
        assert response.get('data').get('deleteRoom').get('id') == str(self.rid)