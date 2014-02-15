from django.shortcuts import render, get_object_or_404

from antragsfabrik.models import Application


def index(request):
    latest_application_list = Application.objects.all().order_by('-submitted')[:5]
    context = {'latest_application_list': latest_application_list}
    return render(request, 'antragsfabrik/index.html', context)

def detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    return render(request, 'antragsfabrik/detail.html', {'application': application})