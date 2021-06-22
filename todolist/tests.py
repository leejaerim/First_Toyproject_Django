import pytest
from mysite.schema import schema
from graphene.test import Client
from django.test import TestCase

@pytest.mark.django_db
class TestTodoSchema(TestCase):
    def setUp(self):
        self.client = Client(schema)


        

