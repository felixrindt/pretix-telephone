from django.conf.urls import url

from .views import TelephoneFieldSettings

urlpatterns = [
    url(r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/telephone/settings$',
        TelephoneFieldSettings.as_view(), name='settings'),
]
