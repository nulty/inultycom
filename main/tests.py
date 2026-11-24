from datetime import date
from unittest import mock

from django.test import TestCase, override_settings

from main.views import years_of_experience


class YearsOfExperienceTests(TestCase):
    def test_counts_whole_years_since_2013(self):
        self.assertEqual(years_of_experience(date(2026, 11, 24)), 13)
        self.assertEqual(years_of_experience(date(2030, 1, 1)), 17)


class HomePageTests(TestCase):
    def get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        return response

    def test_has_a_real_title_and_description(self):
        response = self.get()
        self.assertContains(
            response, "<title>Iain McNulty · Senior Full-stack Engineer</title>", html=True
        )
        self.assertContains(response, '<meta name="description"')
        self.assertContains(response, '<meta property="og:title"')

    @mock.patch("main.views.date")
    def test_hero_uses_computed_years(self, fake_date):
        fake_date.today.return_value = date(2026, 11, 24)
        self.assertContains(self.get(), "13+ years shipping web products")

    def test_lists_side_projects_without_linking_private_repos(self):
        response = self.get()
        for name in ("Sinsear", "Beermatz", "Tidy It", "DFA chat extension"):
            self.assertContains(response, name)
        self.assertContains(response, 'href="https://sinsear.org"')
        self.assertContains(response, 'href="https://beermatz.com"')
        self.assertNotContains(response, "github.com/nulty/beermatz")
        self.assertNotContains(response, "github.com/nulty/sinsear")

    @override_settings(CONTACT_EMAIL="someone@example.com")
    def test_contact_email_is_a_link_and_visible_text(self):
        response = self.get()
        self.assertContains(response, 'href="mailto:someone@example.com"')
        self.assertContains(response, ">someone@example.com<")

    @override_settings(CONTACT_EMAIL=None)
    def test_get_in_touch_falls_back_to_linkedin_without_an_email(self):
        response = self.get()
        self.assertNotContains(response, "mailto:")
        self.assertContains(response, "Get in touch")

    @override_settings(COMPANY_NUMBER="01234567", REGISTERED_OFFICE="1 Example Street, London")
    def test_footer_shows_company_disclosures(self):
        response = self.get()
        self.assertContains(response, "Company number 01234567")
        self.assertContains(response, "Registered office: 1 Example Street, London")

    @override_settings(COMPANY_NUMBER="01234567", REGISTERED_OFFICE="1 Example Street, London")
    def test_blog_pages_share_the_footer(self):
        self.assertContains(self.client.get("/blog/"), "Company number 01234567")
