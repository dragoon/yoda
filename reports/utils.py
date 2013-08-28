from os import path

from django.template import Template, Context
from django.conf import settings
import django.template.loader

settings.configure()


def render_report(template_name, context):
    t = Template(open(path.join(path.dirname(__file__), 'templates/yoda/default/%(name)s' % {
        'name': template_name})).read())
    return t.render(Context(context))

