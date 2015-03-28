from django.utils.translation import ugettext_lazy as _

import horizon


class Cloudcustom(horizon.Dashboard):
    name = _("Cloudcustom")
    slug = "cloudcustom"
    panels = ('custompanel',)  # Add your panels here.
    default_panel = 'custompanel'  # Specify the slug of the dashboard's default panel.


horizon.register(Cloudcustom)
