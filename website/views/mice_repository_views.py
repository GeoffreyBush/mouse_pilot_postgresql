from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from website.models import Mouse

@login_required
def mice_repository(request):
    mymice = Mouse.objects.all()
    template = loader.get_template("general/mice_repository.html")
    context = {"mymice": mymice}
    return HttpResponse(template.render(context, request))