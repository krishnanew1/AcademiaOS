from django.test import TestCase, Client, override_settings


@override_settings(DEMO_MODE=True)
class DemoReadOnlyMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_requests_allowed(self):
        r = self.client.get('/api/auth/login/')
        self.assertNotEqual(r.status_code, 403)

    def test_login_post_allowed(self):
        r = self.client.post('/api/auth/login/', data={}, content_type='application/json')
        self.assertNotEqual(r.status_code, 403)

    def test_write_blocked(self):
        r = self.client.post('/api/students/', data={}, content_type='application/json')
        self.assertEqual(r.status_code, 403)
        self.assertIn('read-only demo', r.json()['detail'])

    def test_put_patch_delete_blocked(self):
        for method in ('put', 'patch', 'delete'):
            r = getattr(self.client, method)('/api/students/1/', content_type='application/json')
            self.assertEqual(r.status_code, 403, method)


@override_settings(DEMO_MODE=False)
class DemoModeOffTests(TestCase):
    def test_writes_not_blocked_by_middleware(self):
        r = Client().post('/api/students/', data={}, content_type='application/json')
        # 401/404 from auth/routing is fine; must not be the demo 403
        self.assertNotEqual(r.status_code, 403)
