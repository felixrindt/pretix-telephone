import io
import json
from collections import OrderedDict

from defusedcsv import csv
from django import forms
from django.utils.translation import ugettext_lazy as _
from pretix.base.exporter import ListExporter
from pretix.base.models import Order, InvoiceAddress


class TelephoneExporter(ListExporter):
    identifier = 'telephonenumbers'
    verbose_name = _('Telephone numbers')

    def iterate_list(self, form_data):
        yield [_('Order code'), _('Name'), _('Email'), _('Telephone')]

        for order in self.event.orders.filter(status__in=form_data['status']):
            row = [order.code]
            try:
                row.append(order.invoice_address.name)
            except InvoiceAddress.DoesNotExist:
                row.append("")
            row.append(order.email or "")
            contact_form_data = json.loads(order.meta_info)['contact_form_data']
            if 'telephone' in contact_form_data:
                row.append(contact_form_data['telephone'])
            else:
                row.append("")
            yield row

    @property
    def additional_form_fields(self):
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
