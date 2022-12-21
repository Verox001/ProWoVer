from models import Project


def get_project_choices():
    return [(project.title.lower(), project.title) for project in Project.objects.all()]