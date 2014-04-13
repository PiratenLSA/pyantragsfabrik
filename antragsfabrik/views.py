from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from antragsfabrik.models import Application, LQFBInitiative, Type
from antragsfabrik.forms import ApplicationForm, LQFBInitiativeForm, UserProfileForm


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


def appl_detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    return render(request, 'antragsfabrik/detail.html', {'application': application, 'user': request.user})


@login_required
def appl_create(request):
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

            return redirect('appl_detail', application_id=appl.id)

        if not lqfbform.has_changed():
            lqfbform = LQFBInitiativeForm(prefix='lqfb')
    else:
        applform = ApplicationForm(prefix='appl')
        lqfbform = LQFBInitiativeForm(prefix='lqfb')

    return render(request, 'antragsfabrik/create.html', {'applform': applform, 'lqfbform': lqfbform})


@login_required
def appl_edit(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if application.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        applform = ApplicationForm(request.POST, instance=application, prefix='appl')

        if applform.is_valid():
            applform.save()
            return redirect('appl_detail', application_id=application_id)
    else:
        applform = ApplicationForm(instance=application, prefix='appl')
        #lqfbform = LQFBInitiativeForm(prefix='lqfb')

    return render(request, 'antragsfabrik/edit.html', {'applform': applform, 'application': application})


@login_required
def appl_submit(request, application_id):
    return appl_changestatus(request, application_id, Application.SUBMITTED)


@login_required
def appl_cancel(request, application_id):
    return appl_changestatus(request, application_id, Application.CANCELED)


def appl_changestatus(request, application_id, next_status):
    application = get_object_or_404(Application, pk=application_id)

    if application.author != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        application.status = next_status
        application.save()
        return redirect('appl_detail', application_id=application_id)

    return render(request, 'antragsfabrik/changestatus.html', {'application': application, 'next_status': next_status})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        profileform = UserProfileForm(request.POST, instance=request.user.profile, prefix='userprofile')

        if profileform.is_valid():
            profileform.save()
    else:
        profileform = UserProfileForm(instance=request.user.profile, prefix='userprofile')

    return render(request, 'antragsfabrik/profile_edit.html', {'profileform': profileform})