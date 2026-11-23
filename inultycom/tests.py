from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase, override_settings

from inultycom.client_ip import get_client_ip

LOGIN = "/admin/login/"


class ClientIpTests(TestCase):
    """kamal-proxy is the only proxy, so the last X-Forwarded-For hop is the one it added."""

    def ip(self, **meta):
        return get_client_ip(RequestFactory().get("/", **meta))

    def test_uses_address_added_by_kamal_proxy(self):
        self.assertEqual(self.ip(HTTP_X_FORWARDED_FOR="203.0.113.7", REMOTE_ADDR="172.18.0.2"), "203.0.113.7")

    def test_ignores_addresses_a_client_put_in_the_header(self):
        spoofed = "1.2.3.4, 203.0.113.7"
        self.assertEqual(self.ip(HTTP_X_FORWARDED_FOR=spoofed, REMOTE_ADDR="172.18.0.2"), "203.0.113.7")

    def test_falls_back_to_remote_addr_without_a_proxy(self):
        self.assertEqual(self.ip(REMOTE_ADDR="127.0.0.1"), "127.0.0.1")


class AdminLoginLockoutTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser("admin", password="correct horse battery staple")

    def login(self, password, username="admin", ip="203.0.113.7"):
        return self.client.post(
            LOGIN,
            {"username": username, "password": password, "next": "/admin/"},
            HTTP_X_FORWARDED_FOR=ip,
        )

    def fail(self, times, **kwargs):
        for _ in range(times):
            self.assertEqual(self.login("wrong", **kwargs).status_code, 200)  # form re-rendered

    def assertLockedOut(self, response):
        self.assertEqual(response.status_code, 429)

    def test_fifth_failure_locks_out_that_ip(self):
        self.fail(4)
        self.assertLockedOut(self.login("wrong"))
        # Even the right password is refused while locked out
        self.assertLockedOut(self.login("correct horse battery staple"))

    def test_ip_lockout_applies_to_any_username(self):
        # A different username each time, so only the IP can be what locks
        for i in range(5):
            self.login("wrong", username=f"guess{i}")
        self.assertLockedOut(self.login("correct horse battery staple"))

    def test_other_ips_unaffected_by_an_ip_lockout(self):
        for i in range(5):
            self.login("wrong", username=f"guess{i}")
        response = self.login("correct horse battery staple", ip="192.0.2.50")
        self.assertRedirects(response, "/admin/", fetch_redirect_response=False)

    def test_username_lockout_applies_from_any_ip(self):
        for i in range(5):
            self.login("wrong", ip=f"198.51.100.{i}")
        self.assertLockedOut(self.login("correct horse battery staple", ip="192.0.2.99"))

    def test_spoofed_forwarded_for_cannot_dodge_the_ip_lockout(self):
        for i in range(5):
            self.login("wrong", username=f"user{i}", ip=f"10.0.0.{i}, 203.0.113.7")
        self.assertLockedOut(self.login("correct horse battery staple", username="admin2"))

    def test_success_resets_the_failure_count(self):
        self.fail(4)
        response = self.login("correct horse battery staple")
        self.assertRedirects(response, "/admin/", fetch_redirect_response=False)
        self.client.logout()
        self.fail(4)  # would have hit the limit without the reset


class HstsTests(TestCase):
    def test_https_responses_send_hsts(self):
        response = self.client.get("/blog/", HTTP_X_FORWARDED_PROTO="https")
        self.assertEqual(response.headers["Strict-Transport-Security"], "max-age=3600")

    def test_not_sent_over_plain_http(self):
        self.assertNotIn("Strict-Transport-Security", self.client.get("/blog/").headers)
