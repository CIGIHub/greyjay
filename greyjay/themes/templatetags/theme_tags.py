from django import template
from django.db.models import ObjectDoesNotExist

register = template.Library()

from greyjay.themes import utils


def get_theme_content(context):
    try:
        theme = context['self'].theme
    except (KeyError, AttributeError):
        theme = None

    if theme is None:
        return utils.get_default_theme_content()
    else:
        return theme.content


@register.simple_tag(takes_context=True)
def get_contact_email(context):
    theme = get_theme_content(context)

    email = theme.content.contact_email
    if not email:
        try:
            defaults = context['request'].site.default_settings
            return defaults.contact_email
        except ObjectDoesNotExist:
            return ""

    return email


@register.simple_tag(takes_context=True)
def get_text_block(context, usage):
    content = get_theme_content(context)
    return content.block_links.filter(block__usage=usage).first().block


@register.simple_tag(takes_context=True)
def get_follow_link(context, usage):
    content = get_theme_content(context)
    return content.follow_links.filter(block__usage=usage).first().block.link


@register.simple_tag(takes_context=True)
def get_logo(context, usage):
    content = get_theme_content(context)
    return content.logo_links.filter(block__usage=usage).first().block.logo


@register.simple_tag(takes_context=True)
def get_logo_link(context, usage):
    content = get_theme_content(context)
    return content.logo_links.filter(block__usage=usage).first().block.link


@register.filter(name='split_string')
def split_string(value, arg):
    return value.split(arg)
