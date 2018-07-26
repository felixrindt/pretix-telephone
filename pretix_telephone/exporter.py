import json
from collections import OrderedDict

from django import forms
from django.utils.translation import ugettext_lazy as _

from pretix.base.exporter import BaseExporter
from pretix.base.models import Order

class TelephoneExporter(BaseExporter):
    identifier = 'telephonenumbers'
    verbose_name = _('Telephone numbers (text file)')

    def render(self, form_data: dict):
        numbers = []
        for ordervalues in self.event.orders.filter(status__in=form_data['status']).values('meta_info'):
            contact_form_data = json.loads(ordervalues['meta_info'])['contact_form_data']
            if 'telephone' in contact_form_data:
                numbers.append(contact_form_data['telephone'])
        data = "\r\n".join(numbers)
        return '{}_pretixtelephonenumbers.txt'.format(self.event.slug), 'text/plain', data.encode("utf-8")

    @property
    def export_form_fields(self):
        return OrderedDict(
            [
                ('status',
                 forms.MultipleChoiceField(
                     label=_('Filter by status'),
                     initial=[Order.STATUS_PENDING, Order.STATUS_PAID],
                     choices=Order.STATUS_CHOICE,
                     widget=forms.CheckboxSelectMultiple,
                     required=False
                 )),
            ]
        )

