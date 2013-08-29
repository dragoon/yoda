import cgi
import codecs

from pygments import lexers, formatters, highlight
from .utils import render_report

html_formatter = formatters.get_formatter_by_name('html')
python_lexer = lexers.get_lexer_by_name('python')


def html_module_detail(filename, values):
    """
    Creates a module detail report at the specified filename.

    It uses `templates.module_detail` to create the page.
    """
    values['style'] = html_formatter.get_style_defs()

    values['source_lines'] = source_lines = list()
    i = 0
    for i, source_line in enumerate(
            [cgi.escape(l.rstrip()) for l in
             codecs.open(values['source_file'], 'r', 'utf-8').readlines()]):
        line_status = 'ignored'
        if i not in values:
            line_status = 'ignored'
        source_lines.append({'source_line': highlight(source_line, python_lexer, html_formatter),
                             'line_status': line_status})

    fo = codecs.open(filename, 'wb+', 'utf-8')
    response = render_report('module_detail.html', values)
    fo.write(response)
    fo.close()
