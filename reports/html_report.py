import codecs
import os
import shutil
from .html_module_detail import html_module_detail
from .utils import render_report


def html_report(outdir, modules):
    """
    Creates an ``index.html`` in the specified ``outdir``. Also attempts to create
    a ``modules`` subdirectory to create module detail html pages, which are named
    `module.__name__` + '.html'.

    It uses `templates.coverage.base.html` to create the index page.
    """
    context = {}
    m_subdirname = 'modules'
    m_dir = os.path.join(outdir, m_subdirname)
    if not os.path.exists(m_dir):
        os.makedirs(m_dir)

    # Create detail files for covered files
    for module_name, values in modules:
        html_module_detail(os.path.join(m_dir, module_name + '.html'), values)

    fo = codecs.open(os.path.join(outdir, 'index.html'), 'wb+', 'utf-8')
    response = render_report('index.html', context)
    fo.write(response)
    fo.close()

    # Copy static files
    shutil.rmtree(os.path.join(outdir, 'static'), ignore_errors=True)
    shutil.copytree('static', os.path.join(outdir, 'static'))
