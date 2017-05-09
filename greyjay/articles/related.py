'''
Registry for custom related_article behavior depending on site articles are used in.

The default related_article function are listed here. To override:

```
from greyjay.articles.models import ArticlePage
from greyjay.articles.related import register_related_article_behavior


def my_related(page, number):
    #...


# Somewhere which gets called on startup, like models.py or urls.py, or apps.py
register_related_article_behavior(ArticlePage, my_related)
```

See `get_related_behavior` for getting a related article function for a particular model.
Used in article_tags.py.
'''

from . import models


def default_article_get_related(page, number):
    included = [page.id]
    article_list = []
    if page.primary_topic:
        articles = (models.ArticlePage.objects
            .live()
            .filter(primary_topic=page.primary_topic)
            .exclude(id=page.id)
            .distinct()
            .order_by('-first_published_at')
        )[:number]
        article_list.extend(articles.all())
        included.extend([article.id for article in articles.all()])

    current_total = len(article_list)

    if current_total < number:
        # still don't have enough, so pick using secondary topics
        topics = models.Topic.objects.filter(article_links__article=page)
        if topics:
            additional_articles = (models.ArticlePage.objects
                .live()
                .filter(primary_topic__in=topics)
                .exclude(id__in=included)
                .distinct()
                .order_by('-first_published_at')
            )[:number - current_total]
            article_list.extend(additional_articles.all())
            current_total = len(article_list)
            included.extend([article.id for article in additional_articles.all()])

    if current_total < number:
        authors = models.ContributorPage.objects.live().filter(article_links__article=page)
        if authors:
            additional_articles = (models.ArticlePage.objects
                .live()
                .filter(author_links__author__in=authors)
                .exclude(id__in=included)
                .distinct()
                .order_by('-first_published_at')
            )[:number - current_total]
            article_list.extend(additional_articles.all())
            current_total = len(article_list)
            included.extend([article.id for article in additional_articles.all()])

    if current_total < number:
        # still don't have enough, so just pick the most recent
        additional_articles = (models.ArticlePage.objects
            .live()
            .exclude(id__in=included)
            .order_by('-first_published_at')
        )[:number - current_total]
        article_list.extend(additional_articles.all())

    return article_list


def default_series_get_related(series_page, number):
    articles = []
    if series_page.primary_topic:
        articles = list(models.ArticlePage.objects
            .live()
            .filter(primary_topic=series_page.primary_topic)
            .distinct()
            .order_by('-first_published_at')[:number]
        )

    current_total = len(articles)
    if current_total < number:
        for article in series_page.articles:
            articles.extend(list(article.related_articles(number)))
            articles = list(set(articles))[:number]
            current_total = len(articles)

            if current_total >= number:
                return articles

    return articles


_related_map = {
    models.ArticlePage: default_article_get_related,
    models.SeriesPage: default_series_get_related,
}


def get_related_behavior(page):
    global _related_map
    return _related_map.get(page.__class__, default_article_get_related)


def register_related_article_behavior(model_class, func):
    global _related_map
    _related_map[model_class] = func
