# -*- coding: utf-8 -*-
# SPDX-License-Identifier: AGPL-3.0-or-later

import  sys, os
from pathlib import Path
from pallets_sphinx_themes import ProjectLink

from botdetection.__pkginfo__ import (
    VERSION,
    GIT_URL,
    GIT_BRANCH,
    ISSUE_URL,
)

# Project --------------------------------------------------------------

project = 'SearXNG'
copyright = 'SearXNG team'
author = 'SearXNG team'
release, version = VERSION, VERSION

SOURCEDIR = Path(__file__).parent.parent / 'src' / 'botdetection'
os.environ['SOURCEDIR'] = str(SOURCEDIR)

# hint: sphinx.ext.viewcode won't highlight when 'highlight_language' [1] is set
#       to string 'none' [2]
#
# [1] https://www.sphinx-doc.org/en/master/usage/extensions/viewcode.html
# [2] https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-highlight_language

highlight_language = 'default'

# General --------------------------------------------------------------

master_doc = "index"
source_suffix = '.rst'
numfig = True

exclude_patterns = []

# usage::   lorem :patch:`f373169` ipsum
extlinks = {}

# upstream links
# extlinks['pypi'] = ('https://pypi.org/project/%s', 'PyPi: %s')
# extlinks['man'] = ('https://manpages.debian.org/jump?q=%s', '%s')

extensions = [
    'sphinx.ext.imgmath',
    'sphinx.ext.extlinks',
    'sphinx.ext.viewcode',
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "pallets_sphinx_themes",
    "sphinx_issues",                # https://github.com/sloria/sphinx-issues/blob/master/README.rst
    "sphinxcontrib.programoutput",  # https://github.com/NextThought/sphinxcontrib-programoutput
    'linuxdoc.kernel_include',      # Implementation of the 'kernel-include' reST-directive.
    'linuxdoc.rstFlatTable',        # Implementation of the 'flat-table' reST-directive.
    'linuxdoc.kfigure',             # Sphinx extension which implements scalable image handling.
    "sphinx_tabs.tabs",             # https://github.com/djungelorm/sphinx-tabs
    'notfound.extension',           # https://github.com/readthedocs/sphinx-notfound-page
]

autodoc_default_options = {
    'member-order': 'groupwise',
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "babel" : ("https://babel.readthedocs.io/en/latest/", None),
    "flask": ("https://flask.palletsprojects.com/", None),
    "redis": ('https://redis.readthedocs.io/en/stable/', None),
    "searxng": ('https://docs.searxng.org/', None)
}

issues_github_path = "searxng/botdetection"

# HTML -----------------------------------------------------------------

notfound_urls_prefix = '/'

#sys.path.append(os.path.abspath('_themes'))
html_theme_path = ['_themes']
html_theme = "botdetection"

# sphinx.ext.imgmath setup
html_math_renderer = 'imgmath'
imgmath_image_format = 'svg'
imgmath_font_size = 14

html_show_sphinx = False
html_theme_options = {"index_sidebar_logo": True}
html_context = {"project_links": [] }
html_context["project_links"].append(ProjectLink("Source", GIT_URL + '/tree/' + GIT_BRANCH))
html_context["project_links"].append(ProjectLink("Issue Tracker", ISSUE_URL))

html_sidebars = {
    "**": [
        "globaltoc.html",
        "project.html",
        "relations.html",
        "searchbox.html",
        "sourcelink.html"
    ],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
# html_logo = "botdetection.svg"
html_title = "Bot Detection ({})".format(VERSION)
html_show_sourcelink = True

# LaTeX ----------------------------------------------------------------

latex_documents = [
    (master_doc, "botdetection-{}.tex".format(VERSION), html_title, author, "manual")
]
