import base64

from django.conf import settings

from main import content


def encode_email(email):
    """Reverse and base64-encode an address, for settings.CONTACT_EMAIL_ENCODED.
    main.js decodes it; scrapers that don't run JavaScript don't get it."""
    return base64.b64encode(email[::-1].encode()).decode()


def site(request):
    return {
        "contact_email_encoded": settings.CONTACT_EMAIL_ENCODED,
        # Where contact links go before main.js swaps in the mailto: (or without JS).
        "contact_url": content.LINKEDIN_URL,
        "company_number": settings.COMPANY_NUMBER,
        "registered_office": settings.REGISTERED_OFFICE,
        "social_links": content.SOCIAL_LINKS,
        "github_url": content.GITHUB_URL,
    }
