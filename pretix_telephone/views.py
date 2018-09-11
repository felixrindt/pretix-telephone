from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from i18nfield.forms import I18nFormField, I18nTextInput
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import (
    EventSettingsFormView, EventSettingsViewMixin,
)


class TelephoneFieldSettingsForm(SettingsForm):
    telephone_field_required = forms.BooleanField(
        label=_("Require phone number"),
        help_text=_("If this is not checked, entering a phone number is optional."),
        required=False,
    )
    telephone_field_help_text = I18nFormField(
        label=_("Help text"),
        help_text=_("This will be shown below the telephone field. You could use it to indicate why you need the "
                    "number or what you will use it for."),
        required=False,
        widget=I18nTextInput
    )


class TelephoneFieldSettings(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = TelephoneFieldSettingsForm
    template_name = 'pretix_telephone/settings.html'
    permission = 'can_change_settings'

    def get_success_url(self) -> str:
        return reverse('plugins:pretix_telephone:settings', kwargs={
            'organizer': self.request.event.organizer.slug,
            'event': self.request.event.slug
        })
