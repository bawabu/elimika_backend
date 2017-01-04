# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from rest_framework import permissions


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user

        return False
