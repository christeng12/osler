from django.conf.urls import url
from pttrack.urls import url_wrap
from django.views.generic import DetailView

from . import views
from . import models as mymodels

unwrapped_urlconf = [  # pylint: disable=invalid-name
    url(r'^new/(?P<pt_id>[0-9]+)$',
        views.DemographicsCreate.as_view(),
        name='demographics-create'),
    url(r'^(?P<pk>[0-9]+)/$',
        DetailView.as_view(model=mymodels.Demographics),
        name='demographics-detail'),
    url(r'^(?P<pk>[0-9]+)/update/$',
        views.DemographicsUpdate.as_view(),
        name='demographics-update'),
]

urlpatterns = url_wrap(unwrapped_urlconf)