web: bin/dev
reload: DJANGO_SETTINGS_MODULE=inultycom.environments.dev python manage.py livereload '*.md' 'blog_articles/**/*.md'  # extra globs: reload on Markdown edits for /blog/preview/
# rollup -w exits when stdin closes unless it is a TTY; keep a pipe open.
assets: tail -f /dev/null | corepack yarn start
