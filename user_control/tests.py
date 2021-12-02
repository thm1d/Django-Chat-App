from django.test import TestCase
from rest_framework.test import APITestCase
from .views import get_access_token, get_random, get_refresh_token


class TestGenericFunctions(APITestCase):
    
    def test_get_random(self):

        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # Check if we are getting a result
        self.assertTrue(rand1)

        # check if two results are equal
        self.assertNotEqual(rand1, rand2)

        # check the length
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1
        }

        token = get_access_token(payload)

        self.assertTrue(token)

    def test_get_refresh_token(self):
        
        token = get_refresh_token()

        self.assertTrue(token)

class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "thm1d",
            "password": "thm1d23"
        }

        response = self.client.post(self.register_url, data=payload)

        # check that we obtain a status of 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "thm1d",
            "password": "thm1d23"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {
            "username": "thm1d",
            "password": "thm1d23"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        print(response.json())
        refresh = response.json()["refresh"]

        

        # get refresh
        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()

        # print(result)

        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])