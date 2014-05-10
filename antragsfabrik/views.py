from django.http import Http404
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied

from antragsfabrik import utils
from antragsfabrik.models import Application, LQFBInitiative, Type, HistoricalApplication
from antragsfabrik.forms import ApplicationForm, LQFBInitiativeForm, UserProfileForm


def index(request):
    types = dict()
    applications = dict()
    for typ in Type.objects.all().order_by('name'):
        types[typ.id] = typ.name
        applications[typ.id] = Application.objects.filter(typ=typ).exclude(status=Application.CANCELED).order_by(
            '-created')

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

    appl_list3 = dict()
    for appl in appl_list2:
        assert isinstance(appl, Application)
        appl_list3.setdefault(appl.status, []).append(appl)

    statuses = dict()
    for status_key, status_name in Application.STATUS_CHOICES:
        statuses[status_key] = status_name

    context = {'typ': typ, 'appl_list': appl_list3, 'page': appl_list2, 'statuses': statuses}
    return render(request, 'antragsfabrik/typ_index.html', context)


def appl_detail(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    return render(request, 'antragsfabrik/detail.html', {'application': application, 'user': request.user})


def appl_revision(request, application_id, revision):
    application = get_object_or_404(Application, pk=application_id)
    try:
        application_revision = application.history.get(history_id=revision)
    except HistoricalApplication.DoesNotExist:
        raise Http404
    return render(request, 'antragsfabrik/detail.html', {'application': application_revision, 'user': request.user})


def appl_history(request, application_id, page=1):
    if request.method == 'POST':
        try:
            revision1 = request.POST.get('from')
            revision2 = request.POST.get('to')

            if revision1 is not None and revision2 is not None:
                return redirect('appl_history_diff', application_id=application_id,
                                revision1=min(int(revision1), int(revision2)),
                                revision2=max(int(revision1), int(revision2)))
        except KeyError:
            pass

    application = get_object_or_404(Application, pk=application_id)
    paginator = Paginator(application.history.order_by('-updated'), 20)
    try:
        history_list = paginator.page(page)
    except EmptyPage:
        history_list = paginator.page(paginator.num_pages)
    return render(request, 'antragsfabrik/history.html',
                  {'application': application, 'history_list': history_list, 'user': request.user})


def appl_history_diff(request, application_id, revision1, revision2):
    application = get_object_or_404(Application, pk=application_id)
    try:
        application_revision1 = application.history.get(history_id=min(int(revision1), int(revision2)))
        application_revision2 = application.history.get(history_id=max(int(revision1), int(revision2)))
    except HistoricalApplication.DoesNotExist:
        raise Http404

    title_diff_html = utils.diff_html(application_revision1.title, application_revision2.title)
    text_diff_html = utils.diff_html(application_revision1.text, application_revision2.text)
    reasons_diff_html = utils.diff_html(application_revision1.reasons, application_revision2.reasons)

    return render(request, 'antragsfabrik/history_diff.html',
                  {'application': application, 'title_diff': title_diff_html, 'text_diff': text_diff_html,
                   'reasons_diff': reasons_diff_html, 'revision1': application_revision1,
                   'revision2': application_revision2})


@login_required
def appl_create(request):
    # wsd = with submission date - haha, to long
    types_wsd = Type.objects.exclude(submission_date__isnull=True).order_by('name')

    if request.method == 'POST':
        applform = ApplicationForm(request.POST, prefix='appl')
        lqfbform = LQFBInitiativeForm(request.POST, prefix='lqfb')

        if applform.is_valid() and (not lqfbform.has_changed() or lqfbform.is_valid()):
            appl = applform.save(commit=False)
            assert isinstance(appl, Application)

            if 'preview' in request.POST:
                return render(request, 'antragsfabrik/create.html',
                              {'applform': applform, 'lqfbform': lqfbform, 'types_wsd': types_wsd, 'preview': appl})

            appl.author = request.user
            appl.updated_by = request.user
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

    return render(request, 'antragsfabrik/create.html',
                  {'applform': applform, 'lqfbform': lqfbform, 'types_wsd': types_wsd})


@login_required
def appl_edit(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    try:
        lqfb = LQFBInitiative.objects.get(antrag=application)
    except LQFBInitiative.DoesNotExist:
        lqfb = None
        print('lqfb does not exists')

    if application.author != request.user or not application.changeable():
        raise PermissionDenied

    if request.method == 'POST':
        applform = ApplicationForm(request.POST, instance=application, prefix='appl')
        lqfbform = LQFBInitiativeForm(request.POST, instance=lqfb, prefix='lqfb')

        if applform.is_valid() and (not lqfbform.has_changed() or lqfbform.is_valid()):
            appl = applform.save(commit=False)
            assert isinstance(appl, Application)

            if 'preview' in request.POST:
                return render(request, 'antragsfabrik/edit.html',
                              {'applform': applform, 'application': application, 'preview': appl})

            if applform.has_changed():
                appl.updated_by = request.user
                appl.save()

            if lqfbform.has_changed():
                lqfbini = lqfbform.save(commit=False)
                assert isinstance(lqfbini, LQFBInitiative)
                lqfbini.antrag = appl
                lqfbini.save()

            return redirect('appl_detail', application_id=application_id)
    else:
        applform = ApplicationForm(instance=application, prefix='appl')
        lqfbform = LQFBInitiativeForm(instance=lqfb, prefix='lqfb')

    return render(request, 'antragsfabrik/edit.html',
                  {'applform': applform, 'lqfbform': lqfbform, 'application': application})


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

    if next_status == Application.CANCELED and not application.cancelable():
        raise PermissionDenied

    if next_status == Application.SUBMITTED and not application.submittable():
        raise PermissionDenied

    if request.method == 'POST':
        if next_status == Application.SUBMITTED:
            application.submitted = now()

        application.status = next_status
        application.save()
        return redirect('appl_detail', application_id=application_id)

    return render(request, 'antragsfabrik/changestatus.html', {'application': application, 'next_status': next_status})


@permission_required('antragsfabrik.set_appl_number')
def appl_set_number(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if application.status != Application.SUBMITTED:
        raise PermissionDenied

    if request.method == 'POST':
        application.set_number()
        return redirect('appl_detail', application_id=application_id)

    return render(request, 'antragsfabrik/setnumber.html', {'application': application})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        profileform = UserProfileForm(request.POST, instance=request.user.profile, prefix='userprofile')

        if profileform.is_valid():
            profileform.save()
    else:
        profileform = UserProfileForm(instance=request.user.profile, prefix='userprofile')

    return render(request, 'antragsfabrik/profile_edit.html', {'profileform': profileform})


def imprint(request):
    return render(request, 'antragsfabrik/imprint.html')