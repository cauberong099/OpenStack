from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.cloudcustom import dashboard

class Custompanel(horizon.Panel):
    name = _("Custompanel")
    slug = "custompanel"


dashboard.Cloudcustom.register(Custompanel)
