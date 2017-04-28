from __future__ import absolute_import, unicode_literals

import logging

from django.template.loader import TemplateDoesNotExist, render_to_string
from django.utils.safestring import mark_safe

from . import utils

logger = logging.getLogger(__file__)


class ThemeableMixin(object):
    def render(self, value, context=None):
        """
        Return a text rendering of 'value', suitable for display on templates. By default, this will
        use a template if a 'template' property is specified on the block, and fall back on render_basic
        otherwise.
        """
        template = getattr(self.meta, 'template', None)
        if not template:
            return self.render_basic(value, context=context)

        if context is None:
            logger.warning(
                'ThemeableMixin render method received a None context, theming is not possible unless the'
                ' {% include_block %} template tag is used or another mechanism which provide the root'
                ' templates context.'
            )
            new_context = self.get_context(value)
        else:
            new_context = self.get_context(value, parent_context=dict(context))

        if 'self' not in new_context:
            logger.warning(
                'ThemeableMixin render method received a context without "self" which is expected to be page'
            )

        theme = utils.theme_from_context(new_context)

        if theme is not None:
            theme_template = utils.get_themed_template_name(theme, template)
            try:
                rendering = render_to_string(theme_template, new_context)
            except TemplateDoesNotExist:
                rendering = render_to_string(template, new_context)
        else:
            rendering = render_to_string(template, new_context)

        return mark_safe(rendering)
