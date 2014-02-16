from django.shortcuts import render, get_object_or_404, redirect

from antragsfabrik.models import Application, LQFBInitiative
from antragsfabrik.forms import ApplicationForm, LQFBInitiativeForm


def index(request):
    latest_application_list = Application.objects.all().order_by('-submitted')[:5]
    context = {'latest_application_list': latest_application_list}
    return render(request, 'antragsfabrik/index.html', context)


def detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    return render(request, 'antragsfabrik/detail.html', {'application': application})


def create(request):
    if request.method == 'POST':
        applform = ApplicationForm(request.POST, prefix='appl')
        lqfbform = LQFBInitiativeForm(request.POST, prefix='lqfb')

        if applform.is_valid() and (not lqfbform.has_changed() or lqfbform.is_valid()):
            appl = applform.save(commit=False)
            assert isinstance(appl, Application)
            appl.author = request.user
            appl.save()

            if lqfbform.has_changed():
                lqfbini = lqfbform.save(commit=False)
                assert isinstance(lqfbini, LQFBInitiative)
                lqfbini.antrag = appl
                lqfbini.save()

            return redirect('detail', application_id=appl.id)

        if not lqfbform.has_changed():
            lqfbform = LQFBInitiativeForm(prefix='lqfb')
    else:
        applform = ApplicationForm(prefix='appl')
        lqfbform = LQFBInitiativeForm(prefix='lqfb')

    return render(request, 'antragsfabrik/create.html', {'applform': applform, 'lqfbform': lqfbform})