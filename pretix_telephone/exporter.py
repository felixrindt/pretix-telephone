import io
import json
from collections import OrderedDict

from defusedcsv import csv
from django import forms
from django.utils.translation import ugettext_lazy as _
from pretix.base.exporter import BaseExporter
from pretix.base.models import Order


class TelephoneExporter(BaseExporter):
    identifier = 'telephonenumbers'
    verbose_name = _('Telephone numbers (CSV)')

    def render(self, form_data: dict):
        output = io.StringIO()
        if form_data.get('dialect', '-') in csv.list_dialects():
            writer = csv.writer(output, dialect=form_data.get('dialect'))
        elif form_data.get('dialect', '-') == "semicolon":
            writer = csv.writer(output, dialect='excel', delimiter=';')
        else:
            writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC, delimiter=",")

        writer.writerow([_('Order code'), _('Name'), _('Telephone')])

        for order in self.event.orders.filter(status__in=form_data['status']):
            row = [order.code]
            try:
                row.append(order.invoice_address.name)
            except InvoiceAddress.DoesNotExist:
                row.append("")
            contact_form_data = json.loads(order.meta_info)['contact_form_data']
            if 'telephone' in contact_form_data:
                row.append(contact_form_data['telephone'])
            else:
                row.append("")
            writer.writerow(row)

        return '{}_telephone.csv'.format(self.event.slug), 'text/csv', output.getvalue().encode("utf-8")


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
                ('dialect',
                 forms.ChoiceField(
                    label=_('CSV dialect'),
                    choices=(('default', 'Default'),
                             ('excel', 'Excel'),
                             ('semicolon', 'Semicolon'),
                    )
                )),
            ]
        )
