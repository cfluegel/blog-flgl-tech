AUTHOR = 'Christoph Flügel'
SITENAME = 'blog.flgl.tech'
SITEURL = ''


TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'

PATH = 'content'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('github', 'https://github.com/cfluegel/'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Changes that I made after the Quickstart
DELETE_OUTPUT_DIRECTORY = True
THEME = "themes/simplegrey"

PLUGIN_PATHS = ['plugins']
#PLUGINS = ['filetime_from_git']
PLUGINS = []

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

STATIC_PATHS = [
        'images',
        'extra',
        'files',
        ]

EXTRA_PATH_METADATA = {
        'extra/robots.txt': {'path': 'robots.txt'},
        'extra/favicon.ico': {'path': 'favicon.ico'},
        'extra/htaccess': {'path': '.htaccess'},
        }

DEFAULT_METADATA = {
        'status': 'draft',
        }

MARKDOWN = {
        'extension_configs': {
 #            "markdown.extensions.codehilite": {"css_class": "highlight"},
            "markdown.extensions.extra": {},
            "markdown.extensions.meta": {},
            "markdown.extensions.toc": {"title": "Table of Contents"},
        },
        'output_format': 'html5',
}