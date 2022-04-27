from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import Member


# class YourTestClass(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         member = Member.objects.create(name='byeonguk')
#
#     def test_name_label(self):
#         first_member = Member.objects.get(name='byeonguk').first_name
#
#         self.assertEquals(first_name, 'first name')
#
#     def test_age_bigger_19(self):
#         age = Member.objects.get(name='byeonguk').age
#
#         check_age = age > 19
#
#         self.assertTrue(check_age)


class AccountTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='test1234!')
        Member.objects.create(name='test', user=user)

    def test_signup_account(self):
        data = {'username': 'test2', 'password': 'test1234!', 'name': 'test2'}
        response = self.client.post('http://localhost:8000/api/v1/account/signup/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Member.objects.get(name='test2').name, 'test2')

    def test_check_username(self):
        data = 'test1'
        response = self.client.get(f'http://localhost:8000/api/v1/account/signup/?username={data}')
        # self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
