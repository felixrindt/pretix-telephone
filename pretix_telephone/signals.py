import json
from django.dispatch import receiver
from pretix.presale.signals import contact_form_fields
from pretix.control.signals import order_info
from django import forms
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _

@receiver(contact_form_fields, dispatch_uid="pretix_telephone_question")
def add_telephone_question(sender, **kwargs):
    return {'telephone': forms.CharField(
            label = _('Telephone'),
            required = False,
            widget = forms.TextInput(attrs={'placeholder': _('Telephone')}),
        )}

@receiver(order_info, dispatch_uid="pretix_telephone_orderinfo")
def add_telephone_order_info(sender, order=None, **kwargs):
    if not order:
        return
    template = get_template('pretix_telephone/orderdetails.html')
    ctx = json.loads(order.meta_info)['contact_form_data']
    return template.render(ctx)

