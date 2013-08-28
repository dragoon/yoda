from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('reports', 'templates/default'))


def render_report(template_name, context):
    t = env.get_template(template_name)
    return t.render(context)

