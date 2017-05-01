from __future__ import absolute_import, division, unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
)

from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet


from . import utils


@python_2_unicode_compatible
class ThemeContent(ClusterableModel):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Only provide if this should be different from the site default email contact address.",
    )

    default = models.BooleanField(default=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('contact_email'),
        FieldPanel('default'),
        InlinePanel('block_links', label="Content Blocks"),
        InlinePanel('follow_links', label="Follow Links"),
        InlinePanel('logo_links', label="Logos"),
    ]

    def __str__(self):
        return self.name

register_snippet(ThemeContent)


@python_2_unicode_compatible
class Theme(models.Model):
    name = models.CharField(max_length=1024)
    folder = models.CharField(max_length=1024, default="themes/default")
    content = models.ForeignKey(ThemeContent, null=True)

    def __str__(self):
        return self.name

    panels = [
        FieldPanel('name'),
        FieldPanel('folder'),
        SnippetChooserPanel('content'),
    ]

register_snippet(Theme)


class ThemeablePage(Page):
    '''
    Abstract model class to inherit from for themable pages
    '''
    is_creatable = False

    class Meta:
        abstract = True

    theme = models.ForeignKey(
        'Theme',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def get_template(self, request, *args, **kwargs):
        original_template = super(ThemeablePage, self).get_template(request, *args, **kwargs)
        if self.theme is None:
            return original_template

        custom_template = utils.get_themed_template_name(self.theme, original_template)
        if utils.template_exists(custom_template):
            return custom_template

        return original_template

    style_panels = [
        MultiFieldPanel(
            [
                SnippetChooserPanel('theme'),
            ],
            heading="Theme"
        ),
    ]


@python_2_unicode_compatible
class TextBlock(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    heading = models.TextField(blank=True, default="")
    content = RichTextField(blank=True, default="")

    panels = [
        FieldPanel('name'),
        FieldPanel('heading'),
        FieldPanel('content'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(TextBlock)


@python_2_unicode_compatible
class FollowLink(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    link = models.CharField(max_length=1024)

    panels = [
        FieldPanel('name'),
        FieldPanel('link'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(FollowLink)


@python_2_unicode_compatible
class LogoBlock(models.Model):
    name = models.CharField(max_length=255)
    usage = models.CharField(max_length=255, blank=True, default="")
    logo = models.ForeignKey(
        'images.AttributedImage',
    )
    link = models.CharField(max_length=2048, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('link'),
        FieldPanel('usage'),
    ]

    def __str__(self):
        return self.name

register_snippet(LogoBlock)


class ContentBlockLink(models.Model):
    block = models.ForeignKey(
        "TextBlock",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='block_links'
    )

    panels = [SnippetChooserPanel("block")]


class ContentFollowLink(models.Model):
    block = models.ForeignKey(
        "FollowLink",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='follow_links'
    )

    panels = [SnippetChooserPanel("block")]


class ContentLogoLink(models.Model):
    block = models.ForeignKey(
        "LogoBlock",
        related_name='content_links'
    )
    theme_content = ParentalKey(
        "ThemeContent",
        related_name='logo_links'
    )

    panels = [SnippetChooserPanel("block")]
