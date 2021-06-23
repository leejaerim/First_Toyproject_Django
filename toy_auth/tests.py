from toy_auth.models import GuestUser
from django.test.client import RequestFactory
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase
from .middleware import passTokenTest


class TestUserSchema(TestCase):
    def setUp(self):
        self.client = Client(schema, middleware=[passTokenTest])
        self.request = RequestFactory().get('/')
        self.uid = GuestUser.objects.signIn(token='').pk

    def test_create_user(self):
        self.request.headers = {'authorization': ''}
        query = """
            mutation 
            {
                signInGuest {
                    id
                    name
                    token
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )

        assert response.get('data').get('signInGuest') is not None 
        
    def test_update_name(self):
        self.request.headers = {'authorization': ''}
        self.request.uid = self.uid
        query = """
            mutation ($name: String)
            {
                updateUser(name:$name) {
                    name
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request,
            variables = {'name': 'JJJ'}
        )

        assert response.get('data').get('updateUser') == {'name':'JJJ'}
        

