"""Copy and links for the site. Templates own the markup; this module owns the words.

Tailwind scans this file (tailwind.config.js) for the toolbox tile classes.
"""

CAREER_START_YEAR = 2013

LINKEDIN_URL = "https://www.linkedin.com/in/iainmcnulty"
GITHUB_URL = "https://github.com/nulty"

# Nav icons: "icon" names a template in main/templates/main/icons/.
SOCIAL_LINKS = [
    {"label": "GitHub", "url": GITHUB_URL, "icon": "github", "size": "h-5 w-5"},
    {"label": "LinkedIn", "url": LINKEDIN_URL, "icon": "linkedin", "size": "h-[19px] w-[19px]"},
    {"label": "X (Twitter)", "url": "https://x.com/inultydev", "icon": "x", "size": "h-[18px] w-[18px]"},
]

PRACTICES = [
    {
        "icon": "users",
        "title": "Technical leadership",
        "body": (
            "I set the technical direction: I shape the architecture, break down the work "
            "and mentor developers as they grow."
        ),
    },
    {
        "icon": "git-branch",
        "title": "Engineering practices",
        "body": (
            "I bring in the practices that make teams faster and safer: CI/CD, automated "
            "testing and thoughtful code review. I use AI agents inside that loop to explore "
            "unfamiliar codebases, write tests, refactor and give changes a first review, and "
            "I review everything they write."
        ),
    },
    {
        "icon": "layers",
        "title": "Full-stack delivery",
        "body": "I build from the database to the browser, in production Ruby, Python and JavaScript.",
    },
]

WORKING_WITH_ME = [
    "Permanent or contract",
    "Limited company",
    "Insured",
    "DBS cleared",
    "Remote or hybrid",
]

# Each item has an image under static/images/, or a text "tile" (label and classes)
# for tools without a logo here yet.
TOOLBOX = [
    {
        "title": "Languages",
        "items": [
            {"name": "Ruby", "image": "images/rubyl.svg"},
            {"name": "Python", "image": "images/python.svg"},
            {"name": "JavaScript", "image": "images/js.png"},
            {"name": "Crystal", "image": "images/crystal-white.svg"},
        ],
    },
    {
        "title": "Frameworks and platforms",
        "items": [
            {"name": "Rails", "image": "images/rails.png"},
            {"name": "Django", "tile": "dj", "tile_class": "bg-[#0c4b33] text-white"},
            {"name": "React", "image": "images/react.png"},
            {"name": "Vue", "image": "images/vuejs.svg"},
            {"name": "Browser extensions", "image": "images/chrome.svg"},
        ],
    },
    {
        "title": "Infrastructure and tools",
        "items": [
            {"name": "AWS", "image": "images/aws.svg"},
            {"name": "Docker", "image": "images/docker.svg"},
            {"name": "PostgreSQL", "tile": "pg", "tile_class": "bg-[#336791] text-white"},
            {
                "name": "Claude Code",
                "tile": ">_",
                "tile_class": "border border-ink-line bg-ink-deep font-mono text-clay",
            },
        ],
    },
]

# Links go to live sites where the repo is private. "icon" names a template in
# main/templates/main/icons/.
PROJECTS = [
    {
        "name": "Sinsear",
        "stack": "Svelte · SQLite (WASM) · Cloudflare Workers · Hono · Turso · MCP",
        "description": (
            "A family-tree app that runs in the browser, with its database stored on "
            "your own device, so it works offline. Trees can be shared for collaboration "
            "through a Cloudflare Workers API, and an MCP endpoint lets AI research agents "
            "work through a tree alongside the researcher."
        ),
        "links": [{"icon": "site", "label": "sinsear.org", "url": "https://sinsear.org"}],
    },
    {
        "name": "Beermatz",
        "stack": "Rails 8 · PostGIS · Solid Queue · Hotwire Native · Kotlin",
        "description": (
            "A guide to London's pubs and bars. Background workers survey the city "
            "through the Google Places API into PostGIS, and a Hotwire Native app brings "
            "it to Android."
        ),
        "links": [
            {"icon": "site", "label": "beermatz.com", "url": "https://beermatz.com"},
            {
                "icon": "play",
                "label": "Google Play",
                "url": "https://play.google.com/store/apps/details?id=com.beermatz.android",
            },
        ],
    },
    {
        "name": "Tidy It",
        "stack": "Go · Linux",
        "description": (
            "A read-only report of the stale things on a Linux laptop that cleaners like "
            "BleachBit miss: unused Docker images, old snaps, apt leftovers. It rates how "
            "safe each one is to remove and gives the command, but never changes anything "
            "itself."
        ),
        "links": [{"icon": "github", "label": "Code", "url": f"{GITHUB_URL}/tidyit"}],
    },
    {
        "name": "DFA chat extension",
        "stack": "JavaScript · Chromium extension",
        "description": (
            "The DFA's chat queue only opens if you keep reloading the page. This browser "
            "extension reloads it for you until the chat becomes available."
        ),
        "links": [{"icon": "github", "label": "Code", "url": f"{GITHUB_URL}/dfa-chat-extension"}],
    },
]
