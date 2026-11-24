from datetime import timedelta
from pathlib import Path
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import BlogArticle


def article(slug, published_at, **kwargs):
    return BlogArticle.objects.create(
        title=kwargs.pop("title", slug.title()),
        sub_title="sub",
        body=kwargs.pop("body", "Body text"),
        slug=slug,
        published_at=published_at,
        **kwargs,
    )


class ArticleVisibilityTests(TestCase):
    def setUp(self):
        now = timezone.now()
        self.published = article("published", now - timedelta(days=1))
        self.draft = article("draft", None)
        self.scheduled = article("scheduled", now + timedelta(days=7))
        self.staff = User.objects.create_user("staff", password="x", is_staff=True)

    def test_published_article_is_public(self):
        response = self.client.get("/blog/published")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Preview:")

    def test_drafts_and_scheduled_are_hidden_from_public(self):
        for slug in ("draft", "scheduled"):
            with self.subTest(slug=slug):
                self.assertEqual(self.client.get(f"/blog/{slug}").status_code, 404)

    def test_staff_can_preview_drafts_and_scheduled(self):
        self.client.force_login(self.staff)
        response = self.client.get("/blog/draft")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preview: draft")

        response = self.client.get("/blog/scheduled")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preview: scheduled for")

    def test_logged_in_non_staff_cannot_preview(self):
        self.client.force_login(User.objects.create_user("reader", password="x"))
        self.assertEqual(self.client.get("/blog/draft").status_code, 404)

    def test_unknown_slug_is_404_not_500(self):
        self.assertEqual(self.client.get("/blog/no-such-article").status_code, 404)

    def test_index_lists_only_published_even_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get("/blog/")
        self.assertContains(response, "Published")
        self.assertNotContains(response, "Draft")
        self.assertNotContains(response, "Scheduled")

    def test_article_page_shows_publish_date_not_created_date(self):
        backdated = article(
            "backdated",
            timezone.make_aware(timezone.datetime(2024, 11, 1, 21, 26)),
        )
        response = self.client.get(backdated.get_absolute_url())
        self.assertContains(response, "Friday, 01 Nov 2024")

    def test_article_page_title_and_description_come_from_the_article(self):
        response = self.client.get("/blog/published")
        self.assertContains(response, "<title>Published · Iain McNulty</title>", html=True)
        self.assertContains(response, '<meta name="description" content="sub" />', html=True)

    def test_get_absolute_url(self):
        self.assertEqual(self.published.get_absolute_url(), "/blog/published")


class MarkdownFilePreviewTests(TestCase):
    def setUp(self):
        self.base = Path(tempfile.mkdtemp())
        (self.base / "post.md").write_text("# My Title\n\nSome **bold** text\n")
        (self.base / "notes.txt").write_text("not markdown")

    def get(self, path):
        with override_settings(DEBUG=True, BASE_DIR=self.base):
            return self.client.get(f"/blog/preview/{path}")

    def test_renders_markdown_file_with_heading_as_title(self):
        response = self.get("post.md")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<h1 class=\"text-4xl font-bold text-justify\">My Title</h1>", html=False)
        self.assertContains(response, "<strong>bold</strong>")
        self.assertContains(response, "Local preview of")

    def test_disabled_when_debug_is_off(self):
        with override_settings(DEBUG=False, BASE_DIR=self.base):
            self.assertEqual(self.client.get("/blog/preview/post.md").status_code, 404)

    def test_only_markdown_files_inside_the_project(self):
        # A real .md file just outside the project root must not be reachable.
        outside = self.base.parent / f"{self.base.name}-outside.md"
        outside.write_text("# secret")
        self.addCleanup(outside.unlink)

        for path in ("notes.txt", "missing.md", "../../etc/passwd", f"../{outside.name}"):
            with self.subTest(path=path):
                self.assertEqual(self.get(path).status_code, 404)
