from django import template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from logviewer.settings import PAGE_COUNT

register = template.Library()


@register.filter(name='delete_space_tag')
def delete_space(content):
    if content:
        first = content.strip()[0]
        if ord(first) > 90 or ord(first) < 65:
            content = '.....' + content
    return content


@register.simple_tag(name='minustwo')
def some_function(value):
    return value - 2


@register.simple_tag(takes_context=True, name='paginate_tag')
def paginate(context, object_list, ):
    # 每页数目，用于计算总页数， 需要跟后台页面上的显示数目一致

    left = 3
    right = 3

    paginator = Paginator(object_list, PAGE_COUNT)
    page = context['request'].GET.get('page')

    try:
        object_list = paginator.page(page)
        context['current_page'] = int(page)
        pages = (get_left(context['current_page'], left, paginator.num_pages) +
                 get_right(context['current_page'], right, paginator.num_pages))

    except PageNotAnInteger:
        object_list = paginator.page(1)
        context['current_page'] = 1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list
    context['pages'] = pages
    context['last_page'] = paginator.num_pages
    context['first_page'] = 1
    try:
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1

    except IndexError:
        context['pages_first'] = 1
        context['pages_last'] = 2

    return ''


def get_left(current_page, left, num_pages):
    if current_page == 1:
        return []
    elif current_page == num_pages:
        my_list = [i - 1 for i in range(current_page,
                                        current_page - left, -1) if i - 1 > 1]
        my_list.sort()
        return my_list
    my_list = [i for i in range(
        current_page, current_page - left, -1) if i > 1]
    my_list.sort()
    return my_list


def get_right(current_page, right, num_pages):
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page,
                                 current_page + right - 1) if i < num_pages - 1]
