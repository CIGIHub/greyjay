from django.apps import AppConfig


class EndNotesAppConfig(AppConfig):
    name = 'greyjay.content_notes'
    label = 'content_notes'
    verbose_name = "Wagtail end notes"

    def ready(self):
        from greyjay.articles.models import ArticlePage
        from wagtail.wagtailadmin.edit_handlers import (
            MultiFieldPanel,
            FieldPanel,
            InlinePanel,
            ObjectList
        )

        notes_panel = [
            MultiFieldPanel(
                [
                    FieldPanel('endnotes_heading'),
                    FieldPanel('endnote_identifier_style'),
                    InlinePanel('endnote_links', label="End Notes"),
                ],
                heading="End Notes Section"
            ),
            MultiFieldPanel(
                [
                    FieldPanel('citations_heading'),
                    InlinePanel('citation_links', label="Citations"),
                ],
                heading="Citations Section"
            ),
        ]

        ArticlePage.edit_handler.children.insert(
            -1,
            ObjectList(notes_panel, heading="Notes")
        )
