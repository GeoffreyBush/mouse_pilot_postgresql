from itertools import chain

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .filters import BWFilter, ProjectFilter
from .forms import (
    CageForm,
    CommentForm,
    CustomUserCreationForm,
    MiceForm,
    MouseSelectionForm,
    RequestForm,
)
from .models import Cage, Comment, HistoricalMice, Mice, Project, Request, Strain

#########################
### Family Tree views ###
#########################


# Can't add @login_required for family tree views: "'Mice' object has no attribute 'user"
def create_family_tree_data(mouse, role=None):
    # Recursively build the family tree data for the given mouse
    data = {
        "name": str(mouse.id),
        "role": role,
        "parent": str(mouse.mother.id) if mouse.mother else None,
        # Add more mouse attributes here if needed
    }
    children = []
    if mouse.mother:
        children.append(create_family_tree_data(mouse.mother, "Mother"))
    if mouse.father:
        children.append(create_family_tree_data(mouse.father, "Father"))
    if children:
        data["children"] = children
    return data


def family_tree(request, mouse_id):
    mouse = Mice.objects.get(id=mouse_id)
    data = create_family_tree_data(mouse)
    return JsonResponse(data)


#######################
### Help Page views ###
#######################
def help_page(request):
    template = loader.get_template("help_pages/help.html")
    context = {}
    return HttpResponse(template.render(context, request))


def register_account(request):
    template = loader.get_template("help_pages/register_account.html")
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


########################
### Researcher views ###
########################


@login_required
def researcher_dashboard(request):
    myprojects = Project.objects.all()
    mymice = Mice.objects.all()

    # Update mice counts of each project - inefficient n^m time
    # Should be made a Project or Mice object method instead
    for project in myprojects:
        for mouse in mymice:
            if project.projectname == mouse.project.projectname:
                project.mice_count += 1

    template = loader.get_template("researcher/researcher_dashboard.html")
    context = {
        # Could add researcher/user variable here
        "myprojects": myprojects,
    }
    return HttpResponse(template.render(context, request))


@login_required
def show_project(http_request, projectname):
    myproject = Project.objects.get(pk=projectname)

    # Load page with no "Add Request" form submission
    if http_request.method == "GET":
        mycomment = Comment.objects.all()
        mycage = Cage.objects.all()

        # Select only those mice that belong to this project
        mymice = Mice.objects.select_related("cage").filter(project=projectname)

        # Select all mice that belong to this project that have a request
        queryset_miceids = chain(
            *[
                mymice.filter(id__in=request.mice.all())
                for request in Request.objects.all()
            ]
        )
        mice_ids_with_requests = []
        for mouse in queryset_miceids:
            mice_ids_with_requests.append(mouse.id)

        # Was the search or cancel filter button pressed?
        filter = ProjectFilter(http_request.GET, queryset=mymice)
        if "search" in http_request.GET:
            mymice = filter.qs
        elif "cancel" in http_request.GET:
            filter = ProjectFilter(queryset=mymice)

        template = loader.get_template("researcher/researcher_show_project.html")
        context = {
            "myproject": myproject,
            "mymice": mymice,
            "mycage": mycage,
            "mycomment": mycomment,
            "mice_ids_with_requests": mice_ids_with_requests,
            "projectname": projectname,
            "filter": filter,
        }
        return HttpResponse(template.render(context, http_request))

    # If "Add Request" button is pressed
    if http_request.method == "POST":
        form = MouseSelectionForm(project=myproject)
        if form.is_valid():
            form.save()
            form.mice.set(form.cleaned_data["mice"])
            return redirect("add_request")
        else:
            return render(
                http_request,
                "researcher/researcher_show_project.html",
                {"form": form, "projectname": projectname},
            )
    return render(http_request, "add_request.html", {"projectname": projectname})


@login_required
def show_comment(request, mouse_id):
    comment = Comment.objects.get(pk=mouse_id)
    mouse = Mice.objects.get(pk=mouse_id)
    projectname = mouse.project.projectname
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = CommentForm(instance=comment)
    return render(
        request, "popups/comment_fragment.html", {"form": form, "comment": comment}
    )


###########################
### Breeding Wing Views ###
###########################


@login_required
def breeding_wing_dashboard(request):
    mycages = Cage.objects.all()
    template = loader.get_template("breeding_wing/breeding_wing_dashboard.html")
    context = {"mycages": mycages}
    return HttpResponse(template.render(context, request))


@login_required
def breeding_wing_view_strain(request, strain_name):
    mystrain = Strain.objects.get(strain_name=strain_name)
    mymice = Mice.objects.filter(strain=strain_name).values()
    template = loader.get_template("breeding_wing/breeding_wing_view_strain.html")
    context = {
        "mystrain": mystrain,
        "mymice": mymice,
    }
    return HttpResponse(template.render(context, request))


@login_required
def breeding_wing_add_litter(request):
    if request.method == "POST":
        form = MiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("breeding_wing_dashboard")
    else:
        form = MiceForm()
    return render(
        request, "breeding_wing/breeding_wing_add_litter.html", {"form": form}
    )


@login_required
def breeding_wing_view_cage(request, cageID):
    mycage = Cage.objects.get(cageID=cageID)
    mymice = Mice.objects.filter(cage=cageID).values()
    # Select only those mice that belong to this cage
    filter = BWFilter(request.GET, queryset=mymice)
    if "search" in request.GET:
        mymice = filter.qs
    elif "cancel" in request.GET:
        filter = BWFilter(queryset=mymice)
    template = loader.get_template("breeding_wing/breeding_wing_view_cage.html")
    context = {
        "mycage": mycage,
        "mymice": mymice,
        "filter": filter,
    }

    return HttpResponse(template.render(context, request))


############################
### Add, Edit Cage Views ###
############################


@login_required
def add_cage(request):
    if request.method == "POST":
        form = CageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("breeding_wing_dashboard")
    else:
        form = CageForm()
    return render(request, "add_cage.html", {"form": form})


@login_required
def edit_cage(request, cageID):
    cage = Cage.objects.get(cageID=cageID)
    if request.method == "POST":
        form = CageForm(request.POST, instance=cage)
        if form.is_valid():
            form.save()
            return redirect("breeding_wing_dashboard")
    else:
        form = CageForm(instance=cage)
    return render(request, "edit_cage.html", {"form": form})


###############################
### Add, Edit, Delete Views ###
###############################


@login_required
def edit_mouse(request, projectname, mouse_id):
    mouse = Mice.objects.get(id=mouse_id)
    if request.method == "POST":
        form = MiceForm(request.POST, instance=mouse)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = MiceForm(instance=mouse)
    return render(
        request, "edit_mouse.html", {"form": form, "projectname": projectname}
    )


@login_required
def add_mouse(request, projectname):
    if request.method == "POST":
        form = MiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("show_project", projectname=projectname)
    else:
        form = MiceForm()
    return render(
        request, "add_mouse.html", {"mice_form": form, "projectname": projectname}
    )


@login_required
def delete_mouse(request, projectname, mouse_id):
    mouse = Mice.objects.get(id=mouse_id)
    mouse.delete()
    return redirect("show_project", projectname=projectname)


@login_required
def edit_history(request):
    histories_with_diff = []
    histories = HistoricalMice.objects.all().order_by("-history_date")

    for history in histories:
        if hasattr(history, "prev_record") and history.prev_record is not None:
            diff = history.diff_against(history.prev_record)
            changed_fields = [
                (change.field, change.old, change.new) for change in diff.changes
            ]
            history.changed_fields = changed_fields
        else:
            history.changed_fields = []

        histories_with_diff.append(history)

    return render(request, "edit_history.html", {"histories": histories_with_diff})


##########################
### Request Task Views ###
##########################
@login_required
def show_requests(http_request):
    requests = Request.objects.all()
    return render(http_request, "show_requests.html", {"requests": requests})


@login_required
def add_request(http_request, projectname):
    # Find associated project, if it exists
    project = None
    if projectname is not None:
        project = Project.objects.get(pk=projectname)

    # Fetch RequestForm
    if http_request.method == "POST":
        form = RequestForm(http_request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            task.mice.set(form.cleaned_data["mice"])
            return redirect("show_project", projectname=projectname)
    else:
        form = RequestForm(project=project)
    return render(
        http_request, "add_request.html", {"form": form, "projectname": projectname}
    )


@login_required
def confirm_request(http_request, request_id):
    req = Request.objects.get(pk=request_id)
    req.confirm()
    return redirect("show_requests")


# This show_message view doesn't work currently - no popup renders on show_request.html
@login_required
def show_message(request):

    context = {}
    return render(request, "popups/request_fragment.html", context)


###################
### Login Views ###
###################


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})
