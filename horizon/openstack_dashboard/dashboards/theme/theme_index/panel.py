import horizon

from openstack_dashboard.dashboards.theme import dashboard

class ThemePanel(horizon.Panel):
    name = "Panel providing a theme"
    slug = 'theme_index'
    nav = True

dashboard.Theme.register(ThemePanel)