from django.http import HttpResponse
from django.template import loader


def help_page_root(request):
    template = loader.get_template("help_pages/help_page_root.html")
    context = {}
    return HttpResponse(template.render(context, request))


def register_account_guide(request):
    template = loader.get_template("help_pages/register_account_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def history_guide(request):
    template = loader.get_template("help_pages/history_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def project_guide(request):
    template = loader.get_template("help_pages/project_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def add_mouse_guide(request):
    template = loader.get_template("help_pages/add_mouse_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def edit_mouse_guide(request):
    template = loader.get_template("help_pages/edit_mouse_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def filter_guide(request):
    template = loader.get_template("help_pages/filter_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def request_guide(request):
    template = loader.get_template("help_pages/request_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def comment_guide(request):
    template = loader.get_template("help_pages/comment_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def family_tree_guide(request):
    template = loader.get_template("help_pages/family_tree_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def bw_guide(request):
    template = loader.get_template("help_pages/bw_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def add_cage_guide(request):
    template = loader.get_template("help_pages/add_cage_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def edit_cage_guide(request):
    template = loader.get_template("help_pages/edit_cage_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))
