# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r'users', views.UserViewSet)
router.register(r'learners', views.LearnerViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(
        r'^login/$',
        view=views.LoginView.as_view(),
        name='login'
    ),
    url(
        r'^logout/$',
        view=views.LogoutView.as_view(),
        name='logout'
    ),
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^~redirect/$',
        view=views.UserRedirectView.as_view(),
        name='redirect'
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^~update/$',
        view=views.UserUpdateView.as_view(),
        name='update'
    ),
]
