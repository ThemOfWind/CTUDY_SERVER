from time import sleep

from test_plus.test import TestCase
from account.models import Member


# noinspection SpellCheckingInspection
class ContractListViewTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        # Member
        self.일반사용자 = Member.objects.create_user(username='일반사용자', email='test@test', password='test')

    def test_로그인을_한다(self):
        res = self.client.post(
            path='/api/v2/account/signin/',
            data={'username': '일반사용자', 'password': 'test'},
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIsNotNone(data["response"])
        self.assertIsNotNone(data["response"]["access_token"])

        return data['response']['access_token']

    def test_아이디를_중복체크_한다(self):
        # 중복 체크
        res = self.client.get(
            path="/api/v2/account/signup/",
            data={"email": "test"},
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)

    def test_password_변경한다(self):
        access_token = self.test_로그인을_한다()

        self.client.force_login(self.일반사용자)
        res = self.client.put(
            path='/api/v2/account/password/',
            data={'password': 'test', 'new_password': 'test2'},
            content_type='application/json',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.client.login(username='일반사용자', password='test2'))
