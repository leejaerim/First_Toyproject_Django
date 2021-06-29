from django.test.client import RequestFactory
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase


class TestUserSchema(TestCase):
    def setUp(self):
        self.client = Client(schema)
        self.request = RequestFactory().get('/')
        
    def test_create_user(self):
        self.request.headers = {'authorization': ''}
        query = """
            query 
            {
                user {
                    id
                    name
                    token
                    userType
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )
        
        ## graphql doens't support integer enum so it has prefeix 'A_'
        assert response.get('data').get('user').get('userType') == 'A_0'
        assert response.get('data').get('user').get('name') is not None
    
    def test_exisiting_user_query(self):
        self.request.headers = {'authorization': ''}
        query = """
            query 
            {
                user {
                    id
                    name
                    token
                    userType
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )
        
        token = response.get('data').get('user').get('token')
        id = response.get('data').get('user').get('id')

        self.request.headers = {'authorization': token}
        query = """
            query 
            {
                user {
                    id
                    name
                    token
                    userType
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )
        
        assert response.get('data').get('user').get('id') == str(id)

    def test_update_name(self):
        self.request.headers = {'authorization': ''}
        query = """
            query 
            {
                user {
                    id
                    name
                    token
                    userType
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = self.request
        )
        
        token = response.get('data').get('user').get('token')
        self.request.headers = {'authorization': token}
        
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
