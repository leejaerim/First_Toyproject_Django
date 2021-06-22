import pytest
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase

@pytest.mark.django_db
class TestUserSchema(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_create_user(self):
        query = """
            mutation 
            {
                signInGuest {
                    id
                    name
                    sid
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = {'headers':{'authorization':''}},
        )

        assert response.get('data') is not None 
        
    def test_update_name(self):
        query = """
            mutation ($id: ID!, $name: String)
            {
                updateUser(id:$id, name:$name) {
                    id
                    name
                }
            }
        """
        response = self.client.execute(
            query,
            context_value = {'headers':{'authorization':'4hmkmq80atf6fd552xcstrb6iw9qmkam'}},
            variables = {'id': 3, 'name': 'JJJ'}
        )

        assert response.get('data').get('name') is 'JJJ' 
        

