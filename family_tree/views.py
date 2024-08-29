from django.http import HttpResponse
from django.template import loader
from mice_repository.models import Mouse
import json

def create_family_tree_data(mouse, role=None):
    data = {
        "name": str(mouse.pk),
        "role": role,
    }
    children = []
    if mouse.mother:
        children.append(create_family_tree_data(mouse.mother, "Mother"))
    if mouse.father:
        children.append(create_family_tree_data(mouse.father, "Father"))
    if children:
        data["children"] = children
    return data

def family_tree(request, mouse_pk):
    mouse = Mouse.objects.get(pk=mouse_pk)
    data = create_family_tree_data(mouse)
    
    # Load a template that will render the SVG
    template = loader.get_template('family_tree_svg.html')
    context = {
        'tree_data': json.dumps(data),

        # Replace with your actual image URL
        'mouse_image_url': '/static/images/mouse_icon.png',  
    }
    
    # Render the template
    svg_content = template.render(context, request)
    
    # Return the SVG content with the appropriate content type
    return HttpResponse(svg_content, content_type='image/svg+xml')