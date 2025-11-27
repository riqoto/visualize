# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Visualize'
copyright = '2025, Riqoto'
author = 'Riqoto'
release = '1.0.0'
version = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Dil ayarı - Türkçe
language = 'tr'

# -- Extension configuration -------------------------------------------------

# Napoleon settings - Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Intersphinx mapping - Python standart kütüphanesi dokümantasyonuna link
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# Flask-style tema için alabaster kullanıyoruz (sol menülü, minimal)
html_theme = 'alabaster'
html_static_path = ['_static']

# Alabaster tema ayarları - Flask dokümantasyon tarzı
html_theme_options = {
    # Renk şeması
    'page_width': '1200px',
    'sidebar_width': '280px',
    
    # Logo ve başlık
    'logo': '',
    'logo_name': True,
    'description': 'Veri Görselleştirme Aracı',
    
    # Navigation
    'github_user': 'riqoto',
    'github_repo': 'visual',
    'github_banner': True,
    'github_button': True,
    'github_type': 'star',
    
    # Sidebar ayarları
    'fixed_sidebar': True,
    'show_relbar_bottom': False,
    'show_relbar_top': False,
    
    # Renkler - Modern ve profesyonel
    'link': '#2980b9',
    'link_hover': '#3498db',
    'sidebar_link': '#2c3e50',
    'sidebar_link_underscore': '#34495e',
    'gray_1': '#ecf0f1',
    'gray_2': '#bdc3c7',
    'gray_3': '#95a5a6',
    
    # Font ayarları
    'font_family': "'Source Sans Pro', 'Helvetica', 'Arial', sans-serif",
    'head_font_family': "'Source Sans Pro', 'Helvetica', 'Arial', sans-serif",
    'code_font_family': "'Consolas', 'Menlo', 'Monaco', monospace",
    'code_font_size': '0.9em',
    
    # Ekstra ayarlar
    'show_powered_by': False,
    'extra_nav_links': {},
}

# HTML sidebar - Sol menü içeriği
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

# Tek sayfa yapısı için - Index sayfasında tüm içeriği göster
html_use_index = True
html_split_index = False
html_show_sourcelink = False
html_show_sphinx = False

# HTML çıktı ayarları
html_title = f"{project} v{version}"
html_short_title = project
html_baseurl = 'https://riqoto.github.io/visualize/'
