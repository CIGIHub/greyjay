import logging

from django.conf import settings
from django import template
from django.db.models import ObjectDoesNotExist

from greyjay.themes import utils


class ThemeError(Exception):
    pass


logger = logging.getLogger(__name__)

register = template.Library()

debug = getattr(settings, 'DEBUG', True)


def do_warning(block_name, usage):
    global debug

    if debug:
        raise ThemeError(
            'No theme nor default {} with usage "{}" found'.format(
                block_name,
                usage,
            )
        )

    else:
        logger.warning(
            'No theme nor default {} with usage "{}" found'.format(
                block_name,
                usage,
            )
        )
        return ''


def get_theme_contents(context):
    try:
        theme = context['self'].theme
    except (KeyError, AttributeError):
        theme = None

    if theme is None:
        return [utils.get_default_theme_content()]
    else:
        return [theme.content, utils.get_default_theme_content()]


@register.simple_tag(takes_context=True)
def get_contact_email(context):
    contents = get_theme_contents(context)
    email = ''
    for content in contents:
        email = content.contact_email
        if email:
            return email

    if not email:
        try:
            defaults = context['request'].site.default_settings
            return defaults.contact_email
        except ObjectDoesNotExist:
            return ''

    return email


@register.simple_tag(takes_context=True)
def get_text_block(context, usage):
    contents = get_theme_contents(context)
    for content in contents:
        content_piece = content.block_links.filter(block__usage=usage).first()
        if content_piece is not None:
            break

    if content_piece is None:
        return do_warning('text_block', usage)

    return content_piece.block


@register.simple_tag(takes_context=True)
def get_follow_link(context, usage):
    contents = get_theme_contents(context)
    for content in contents:
        content_piece = content.follow_links.filter(block__usage=usage).first()
        if content_piece is not None:
            break

    if content_piece is None:
        return do_warning('follow_link', usage)

    return content_piece.block.link


@register.simple_tag(takes_context=True)
def get_logo(context, usage):
    contents = get_theme_contents(context)
    for content in contents:
        content_piece = content.logo_links.filter(block__usage=usage).first()
        if content_piece is not None:
            break

    if content_piece is None:
        return do_warning('logo_block', usage)

    return content_piece.block.logo


@register.simple_tag(takes_context=True)
def get_logo_link(context, usage):
    contents = get_theme_contents(context)
    for content in contents:
        content_piece = content.logo_links.filter(block__usage=usage).first()
        if content_piece is not None:
            break

    if content_piece is None:
        return do_warning('logo_block', usage)

    return content_piece.block.link


@register.filter(name='split_string')
def split_string(value, arg):
    return value.split(arg)
