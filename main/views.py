from datetime import date

from django.shortcuts import render

from main import content


def years_of_experience(today):
    return today.year - content.CAREER_START_YEAR


def home(request):
    context = {
        "years": years_of_experience(date.today()),
        "practices": content.PRACTICES,
        "working_with_me": content.WORKING_WITH_ME,
        "toolbox": content.TOOLBOX,
        "projects": content.PROJECTS,
    }
    return render(request, "main/home.html", context)
