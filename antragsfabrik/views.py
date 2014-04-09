from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage

from antragsfabrik.models import Application, LQFBInitiative, Type
from antragsfabrik.forms import ApplicationForm, LQFBInitiativeForm


def index(request):
    types = dict()
    applications = dict()
    for typ in Type.objects.all().order_by('name'):
        types[typ.id] = typ.name
        applications[typ.id] = Application.objects.filter(typ=typ).order_by('-submitted')[:10]

    context = {'types': types, 'applications': applications}
    return render(request, 'antragsfabrik/index.html', context)


def typ_index(request, typ_id, page=1):
    typ = get_object_or_404(Type, pk=typ_id)
    appl_list = Application.objects.filter(typ=typ).order_by('-submitted')
    paginator = Paginator(appl_list, 20)
    try:
        appl_list2 = paginator.page(page)
    except EmptyPage:
        appl_list2 = paginator.page(paginator.num_pages)
    context = {'typ': typ, 'appl_list': appl_list2}
    return render(request, 'antragsfabrik/typ_index.html', context)


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