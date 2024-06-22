from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_queryset(queryset, http_request, paginate_by):
    paginator = Paginator(queryset, paginate_by)
    page = http_request.GET.get("page")

    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)

    return paginated_items


def get_query_params(http_request):
    query_params = http_request.GET.copy()
    query_params.pop("page", None)
    return query_params
