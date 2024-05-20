from django.http import HttpResponse
from django.template import loader

def help_page_root(request):
    template = loader.get_template("help_page_roots/help.html")
    context = {}
    return HttpResponse(template.render(context, request))


def register_account_guide(request):
    template = loader.get_template("help_page_roots/register_account_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def history_guide(request):
    template = loader.get_template("help_page_roots/history_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def project_guide(request):
    template = loader.get_template("help_page_roots/project_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def add_mouse_guide(request):
    template = loader.get_template("help_page_roots/add_mouse_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def edit_mouse_guide(request):
    template = loader.get_template("help_page_roots/edit_mouse_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def filter_guide(request):
    template = loader.get_template("help_page_roots/filter_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def request_guide(request):
    template = loader.get_template("help_page_roots/request_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def comment_guide(request):
    template = loader.get_template("help_page_roots/comment_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def family_tree_guide(request):
    template = loader.get_template("help_page_roots/family_tree_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def bw_guide(request):
    template = loader.get_template("help_page_roots/bw_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def add_cage_guide(request):
    template = loader.get_template("help_page_roots/add_cage_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))


def edit_cage_guide(request):
    template = loader.get_template("help_page_roots/edit_cage_guide.html")
    context = {}
    return HttpResponse(template.render(context, request))