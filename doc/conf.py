project = 'OpenIO'
author = 'OpenIO SAS'
copyright = '2015-2018, OpenIO SAS'
release = '{{RELEASE}}'
show_authors = False

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
html_copy_source = False
html_show_sphinx = False
html_show_sourcelink = False
html_show_copyright = True

templates_path = ['_templates/']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'default'

exclude_patterns = [
        # FIXME(jfs): masked because outdated, and potential harmful if indexed.
        '**/admin-guide/operations_configure_monitoring.*',
        ]

