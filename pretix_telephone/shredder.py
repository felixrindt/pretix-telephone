
from django.utils.translation import ugettext_lazy as _
from pretix.base.shredder import BaseDataShredder
from django.db import transaction
import json

class TelephoneShredder(BaseDataShredder):
    verbose_name = _('Telephone Number')
    identifier = 'telephone_number'
    description = _('This will remove customer phone numbers attached to orders.')

    def _phone(self, order):
        return json.loads(order.meta_info or "{}") \
                   .get("contact_form_data", {}) \
                   .get("telephone", "")

    def generate_files(self):
        yield 'phone-numbers.json', 'application/json', json.dumps({
            order.code: self._phone(order)
            for order in self.event.orders.all() if self._phone(order)
        }, indent=4)

    @transaction.atomic
    def shred_data(self):
        for order in self.event.orders.all():
            meta_info = json.loads(order.meta_info or "{}")
            phone = meta_info.get("contact_form_data", {}).get("telephone", "")
            if phone:
                phone = '█' * len(phone)
                meta_info["contact_form_data"]["telephone"] = phone
                order.meta_info = json.dumps(meta_info)
                order.save(update_fields=['meta_info'])


