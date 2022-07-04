from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied


class PermisosGrupos(object):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Administrador').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PermisosSecre(object):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Secretaria').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PermisosMedicos(object):

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name='Medico').exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
