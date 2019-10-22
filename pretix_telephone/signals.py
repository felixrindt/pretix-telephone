import json

from django import forms
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _
from i18nfield.strings import LazyI18nString
from pretix.base.signals import (
    layout_text_variables, register_data_exporters, register_data_shredders,
)
from pretix.control.signals import nav_event_settings, order_info
from pretix.presale.signals import contact_form_fields

from .shredder import TelephoneShredder


@receiver(contact_form_fields, dispatch_uid="pretix_telephone_question")
def add_telephone_question(sender, **kwargs):
    return {'telephone': forms.CharField(
            label=_('Phone number'),
            required=sender.settings.telephone_field_required,
            help_text=sender.settings.get('telephone_field_help_text', as_type=LazyI18nString),
            widget=forms.TextInput(attrs={'placeholder': _('Phone number'), 'type': 'tel'}),
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
    ctx = json.loads(order.meta_info).get('contact_form_data', {})
    return template.render(ctx)


@receiver(layout_text_variables, dispatch_uid="pretix_telephone_layouttextvar")
def add_layout_text_variable(sender, **kwargs):
    return {
            "telephone": {
                "label": _("Phone number"),
                "editor_sample": "+01 1234 567890",
                "evaluate": lambda pos, order, event: 
                    "" if not order.meta_info else
                    json.loads(order.meta_info).get("contact_form_data", {})
                                               .get("telephone", ""),
            }
    }


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


@receiver(register_data_shredders, dispatch_uid="register_telephone_shredder")
def register_shredder(sender, **kwargs):
    return [
        TelephoneShredder,
    ]
