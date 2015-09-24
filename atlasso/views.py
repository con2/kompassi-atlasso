# encoding: utf-8

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.views.generic.base import TemplateView

from .utils import crowd_login, crowd_logout, CrowdError


logger = logging.getLogger(__name__)


@login_required
@require_GET
def crowd_session_view(request):
    try:
        crowd_cookie = crowd_login(username=request.user.username, request=request)
    except CrowdError as e:
        logger.exception(e)
        return redirect('error_view')

    next_url = request.GET.get('next', settings.ATLASSO_DEFAULT_REDIRECT_URL)
    response = redirect(next_url)
    response.set_cookie(**crowd_cookie)

    return response


@require_GET
def logout_view(request):
    try:
        crowd_logout(request)
    except CrowdError as e:
        logger.exception(e)

    logout(request)
    next_url = request.GET.get('next', settings.ATLASSO_DEFAULT_LOGOUT_REDIRECT_URL)
    return redirect(next_url)


class AtlassoView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(AtlassoView, self).get_context_data(**kwargs)
        context.update(
            kompassi=settings.KOMPASSI_HOST,
        )
        return context
