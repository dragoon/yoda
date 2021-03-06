import codecs
import os
import shutil
from datetime import datetime
from .html_module_detail import html_module_detail
from .utils import render_report


class Context(dict):
    def __init__(self, *args, **kwargs):
        super(Context, self).__init__(*args, **kwargs)
        self['date_gen'] = datetime.now()


def html_report(outdir, modules):
    """
    Creates an ``index.html`` in the specified ``outdir``. Also attempts to create
    a ``modules`` subdirectory to create module detail html pages, which are named
    `module.__name__` + '.html'.

    It uses `templates.coverage.base.html` to create the index page.
    """
    m_subdirname = 'modules'
    m_dir = os.path.join(outdir, m_subdirname)
    if not os.path.exists(m_dir):
        os.makedirs(m_dir)

    # Create detail files for covered files
    for module_name, values in modules:
        values = Context(values)
        html_module_detail(os.path.join(m_dir, module_name + '.html'), values)

    fo = codecs.open(os.path.join(outdir, 'index.html'), 'wb+', 'utf-8')
    response = render_report('index.html', Context())
    fo.write(response)
    fo.close()

    # Copy static files
    shutil.rmtree(os.path.join(outdir, 'static'), ignore_errors=True)
    static_path = os.path.abspath(os.path.dirname(__file__))
    shutil.copytree(os.path.join(static_path, 'static'), os.path.join(outdir, 'static'))
