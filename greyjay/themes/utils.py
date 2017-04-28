from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template, TemplateDoesNotExist


DEFAULT_THEME_NAME = getattr(settings, 'GREYJAY_DEFAULT_THEME_NAME', 'default')


def get_themed_template_name(theme, original_template):
    return '{}/{}'.format(theme.folder, original_template)


def template_exists(template_name):
    try:
        get_template(template_name)
    except TemplateDoesNotExist:
        return False
    else:
        return True


def theme_from_context(context):
    if 'self' in context and hasattr(context['self'], 'theme') and context['self'].theme is not None:
        return context['self'].theme
    else:
        return None


def get_default_content_theme():
    Theme = apps.get_model(app_label='themes', model_name='Theme')

    try:
        return Theme.objects.get(name=DEFAULT_THEME_NAME)
    except Theme.DoesNotExist:
        raise ImproperlyConfigured(
            'Use of the theme_tags requires a theme with the name {name} to be created. The theme does not need'
            ' ot be assigned to any page, but are default values for Theme Content when no theme is set'.format(
                name=DEFAULT_THEME_NAME
            )
        )
