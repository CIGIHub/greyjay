from django import template

from greyjay.jobs.models import JobPostingListPage, JobPostingPage

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_posting_page(context):
    if JobPostingPage.objects.live().count() == 0:
        return None

    listing_page = JobPostingListPage.objects.live().first()
    return listing_page
