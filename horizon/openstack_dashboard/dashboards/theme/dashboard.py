import horizon
from django.utils.translation import ugettext_lazy as _



class Theme(horizon.Dashboard):
    name = _("theme")
    slug = "theme"
    panels = ('theme_index', )
    default_panel = 'theme_index'
    nav = False

horizon.register(Theme)