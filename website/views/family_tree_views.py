from django.http import JsonResponse

from website.models import Mice


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
