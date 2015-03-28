from openstack_dashboard.dashboards.cloudcustom.test import panel as test_panel
from openstack_dashboard.dashboards.cloudcustom import dashboard as cloudcustom_dashboard

from django.conf import settings

import horizon

CLOUDCUSTOM_DASHBOARD_SETTINGS = horizon.get_dashboard('cloudcustom')

if settings.HORIZON_CONFIG.get('test_enabled'):
	CLOUDCUSTOM_DASHBOARD_SETTINGS.register(test_panel.Tests)