# Greyjay

Common Wagtail apps for CIGI projects

## Articles

The main app is `greyjay.articles` which contain rich stream field based
article pages with many of our custom blocks.

`greyjay.articles` requires `greyjay.images`, `greyjay.projects`,
`greyjay.people`, and `greyjay.themes` at minimum to function.


## Themes

`greyjay.themes` can enable theming of Wagtail Pages. There three main
ways a theme can change how a page rendereds, themed templates, block
themes, and themed content. Themed includes are another possible way, but
isn't implemented currently.

### Enable themes

To enable theming on a particular page, extend it from `ThemeablePage`
and hook up the style panels.

```
from greyjay.themes.models import ThemeablePage

class MyPage(ThemeablePage):
    # ...

    style_panels = ThemeablePage.style_panels

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        ObjectList(style_panels, heading='Page Style Options'),
        # ...,
    ])
```

This adds a `theme` Foreign Key to your page for the Theme snippet,
which will default to `None`. Unless `theme` is set the usual templates
will be loaded and the default ThemeContent will be used.

### Themed Templates

The `ThemeablePage` has the `theme` attribute set, the first place we
will look for the template for the page is the Theme folder value
prepended to the default template path for a given page.

By default, a Page's template name is "app_name/model_name.html". With
the theme we will look in "theme.folder/app_name/model_name.html" first.

If theme template hasn't been created, the system will pass through and
use the default template.

This is implement by the `get_template` method on the `ThemeablePage`
base class.

### Themed Blocks

When using a Wagtail StreamField you can customize a block to use a
themed template if it uses a template to render. StructBlocks are the
most common type of block we have themed.

```
from greyjay.themes.blocks import ThemeableMixin

class RelatedItemsBlock(ThemeableMixin):
    heading = blocks.CharBlock(default="Related")
    items = blocks.ListBlock(blocks.PageChooserBlock(label="item"))

    class Meta:
        template = "articles/blocks/related_items_block.html"
```

Inorder for themed block to work you will need to define your own blocks
which inherit from the mixing `greyjay.themes.blocks.ThemeableMixin`
which overrides the render method.

If a theme template isn't defined for a given block the default is used.

*Note:* for the render method to be able to access the Page object and
thus the theme, {% include_block %} rendering must be used. Convert a
block to a string won't work, generally {{ block }}. [Wagtail Release
Notes](http://docs.wagtail.io/en/v1.6/releases/1.6.html#include-block-tag-for-improved-streamfield-template-inclusion)

### Themed Content

The second aspect to themes is ThemeContent, which are collections of
logos, logo links, text blocks, and follow links which tend to be found
in headers and footers which could need to customized if a theme implies
a different organization.

The content is access through a series of theme aware template tags.

```
{% extends "base.html"%}
{% load theme_tags ... %}
...
```

The tags include:

* get_text_block
* get_follow_link
* get_logo
* get_logo_link

Each takes a string which should corespond to the `usage` attribute on
each snippet.

TODO: If a given usage isn't definited for a given theme we should fall
through the default ThemeContent.

For a page without a theme set, the default ThemeContent is used, which
is either set based the `default` attribute being set to True or the
`GREYJAY_DEFAULT_THEME_CONTENT_NAME` setting.

### Theme including

*This hasn't been implemented yet*, but it maybe a preferable to helping
themes where we want to change the header and footer.


## Settings

### `GREYJAY_DEFAULT_THEME_CONTENT_NAME`

*default:* `"default"`

This is used mostly for backwards compatability. If you have a default
ThemeContent which should be used for Themeable Pages which don't have a
theme set, you can set GREYJAY_DEFAULT_THEME_CONTENT_NAME to its name.

*NOTE:* the prefered way to set a ThemeContent to be default is to set
the `default` attribute to True on one ThemeContent. If multiple
ThemeContent objects have `default` set to true than `first()` is used
to select one of them.
