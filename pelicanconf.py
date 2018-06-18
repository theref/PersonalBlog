#!/Users/jamescampbell/anaconda3/envs/blog/bin python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'James Campbell'
SITENAME = 'James Campbell'
SITEURL = ''

THEME = 'themes/pelican-elegant-1.3/'

PATH = 'content'

# MARKDOWN = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
DIRECT_TEMPLATES = (('index', 'tags', 'categories',
                     'archives', 'search', '404'))
STATIC_PATHS = ['theme/images', 'images', 'pdfs']
TAG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
AUTHOR_SAVE_AS = ''

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en_GB'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
