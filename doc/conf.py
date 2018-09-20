html_context = {
    'css_files': ['_static/styles.css'],
    'oio_versions': ['18.04', '17.04', '16.04', 'master'],
    'is_stable': False,
    'landing_page': 'source/sandbox-guide/quickstart.html'
}
extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'sphinx.ext.todo',
        ]

html_theme = 'basic'
html_sidebars = {'**': ['globaltoc.html', 'searchbox.html']}
html_static_path = ['_static/', ]
templates_path = ['_templates/']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'default'
