from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template, TemplateDoesNotExist


DEFAULT_THEME_CONTENT_NAME = getattr(settings, 'GREYJAY_DEFAULT_THEME_CONTENT_NAME', 'default')


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
    '''
    'self' is normally the page in a context, but for block 'self' get moved to 'page'
    and 'self' is set to the block value.
    '''
    if 'page' in context and hasattr(context['page'], 'theme') and context['page'].theme is not None:
        return context['page'].theme
    else:
        return None


def get_default_theme_content():
    ThemeContent = apps.get_model(app_label='themes', model_name='ThemeContent')

    # This is the new way of doing default theme content
    default_theme_content = ThemeContent.objects.filter(default=True).first()

    if default_theme_content is not None:
        return default_theme_content

    # This is for backwards compatability with Open Canada
    try:
        return ThemeContent.objects.get(name=DEFAULT_THEME_CONTENT_NAME)
    except ThemeContent.DoesNotExist:
        raise ImproperlyConfigured(
            'Use of the theme_tags requires either a ThemeContent object needs to have default set to True or a'
            ' ThemeContent with the name {name} to be created. You can set the default theme content name with'
            ' GREYJAY_DEFAULT_THEME_CONTENT_NAME'.format(
                name=DEFAULT_THEME_CONTENT_NAME
            )
        )
