import json

from django import forms
from django.dispatch import receiver
from django.urls import resolve, reverse
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from i18nfield.strings import LazyI18nString

from pretix.base.signals import register_data_exporters
from pretix.control.signals import order_info, nav_event_settings
from pretix.presale.signals import contact_form_fields


@receiver(contact_form_fields, dispatch_uid="pretix_telephone_question")
def add_telephone_question(sender, **kwargs):
    return {'telephone': forms.CharField(
            label=_('Phone number'),
            required=sender.settings.telephone_field_required,
            help_text=sender.settings.get('telephone_field_help_text', as_type=LazyI18nString),
            widget=forms.TextInput(attrs={'placeholder': _('Phone number')}),
        )}


@receiver(register_data_exporters, dispatch_uid="pretix_telephone_exporter")
def register_telephone_exporter(sender, **kwargs):
    from .exporter import TelephoneExporter
    return TelephoneExporter


@receiver(order_info, dispatch_uid="pretix_telephone_orderinfo")
def add_telephone_order_info(sender, order=None, **kwargs):
    if not order:
        return
    template = get_template('pretix_telephone/orderdetails.html')
    ctx = json.loads(order.meta_info)['contact_form_data']
    return template.render(ctx)


@receiver(nav_event_settings, dispatch_uid='pretix_telephone_settings')
def add_settings_nav_tab(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [{
        'label': _('Phone number field'),
        'icon': 'phone',
        'url': reverse('plugins:pretix_telephone:settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_telephone',
    }]
