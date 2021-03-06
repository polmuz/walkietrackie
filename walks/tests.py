import json

from django.test import TestCase, Client
from django.contrib.auth.models import User

class WalkApiV1TestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("myuser", password="mypassword")

    def test_auth_required(self):
        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 401)

    def test_token_auth(self):
        """
        Verify that token based authentication works as expected
        """
        r = self.client.post(
            "/api/v1/token-auth",
            {
                'username': 'myuser',
                'password': 'mypassword'
            }
        )

        token = json.loads(r.content)['token']

        # with token
        r = self.client.get(
            "/api/v1/walks",
            HTTP_AUTHORIZATION="Token " + token
        )
        self.assertEqual(r.status_code, 200)

        # without token
        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 401)

    def test_empty_walks(self):
        self.client.login(username="myuser", password="mypassword")
        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(r.content, [])

    def test_post_walks(self):
        self.client.login(username="myuser", password="mypassword")

        self.client.post("/api/v1/walks",
                         {
                             'time': 600,
                             'distance': 100,
                             'date': '2014-01-01T00:00'
                         }
        )

        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(
            r.content,
            [{
                u'date': u'2014-01-01T00:00:00Z',
                u'distance': 100.0,
                u'time': 600,
                u'pk': 1
            }]
        )

    def test_update_walks(self):
        self.client.login(username="myuser", password="mypassword")

        self.client.post("/api/v1/walks",
                         {
                             'time': 600,
                             'distance': 100,
                             'date': '2014-01-01T00:00'
                         }
        )

        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(
            r.content,
            [{
                u'date': u'2014-01-01T00:00:00Z',
                u'distance': 100.0,
                u'time': 600,
                u'pk': 1
            }]
        )

        r = self.client.put(
            "/api/v1/walks/1",
            json.dumps({
                'time': 601,
                'distance': 200,
                'date': '2014-01-02T00:00',
                'pk': 1
            }),
            content_type='application/json'
        )

        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(
            r.content,
            [{
                u'date': u'2014-01-02T00:00:00Z',
                u'distance': 200.0,
                u'time': 601,
                u'pk': 1
            }]
        )

    def test_delete_walks(self):
        self.client.login(username="myuser", password="mypassword")

        self.client.post("/api/v1/walks",
                         {
                             'time': 600,
                             'distance': 100,
                             'date': '2014-01-01T00:00'
                         }
        )

        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(
            r.content,
            [{
                u'date': u'2014-01-01T00:00:00Z',
                u'distance': 100.0,
                u'time': 600,
                u'pk': 1
            }]
        )

        r = self.client.delete("/api/v1/walks/1")

        r = self.client.get("/api/v1/walks")
        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(r.content, [])
