from django.conf import settings

from main import content


def site(request):
    email = settings.CONTACT_EMAIL
    return {
        "contact_email": email,
        # "Get in touch" emails when an address is configured, else goes to LinkedIn.
        "contact_url": f"mailto:{email}" if email else content.LINKEDIN_URL,
        "company_number": settings.COMPANY_NUMBER,
        "registered_office": settings.REGISTERED_OFFICE,
        "social_links": content.SOCIAL_LINKS,
        "github_url": content.GITHUB_URL,
    }
