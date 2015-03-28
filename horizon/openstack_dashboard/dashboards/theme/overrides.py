from django.utils.translation import ugettext_lazy as _

import horizon

# Change name of project dashboard, panels of project dashboard
project_dash = horizon.get_dashboard("project")
project_dash.name = _("Manager Resource")
#project_group_panel = project_dash.get_panel_group("orchestration")
#project_group_panel.name = "Test"

# Remove orchestration panel group in project dashboard
project_stacks_panel = project_dash.get_panel('stacks')
project_dash.unregister(project_stacks_panel.__class__)
project_resourcetypes_panel = project_dash.get_panel('stacks.resource_types')
project_dash.unregister(project_resourcetypes_panel.__class__)


"""from openstack_dashboard.dashboards.project import dashboard
from openstack_dashboard.dashboards.theme.paneltest import panel



project_group_panel = project_dash.get_panel_group("compute")
project_group_panel.panels.append('paneltest')
"""

#project_compute_gp = project_dash.get_panel_group("compute")
#lst = ['overview','instances']
#project_compute_gp.panels = tuple(lst)


# Change name compute gp and add overview panel
project_compute_gp = project_dash.get_panel_group("compute")
project_compute_gp.name = 'Resources Info'
project_compute_gp.panels = ['overview']

# Get Instances gp and add isntances panel
project_compute_gp = project_dash.get_panel_group("instancespg")
project_compute_gp.panels = ['instances']


# Get Images gp and add Images panel
project_images_gp = project_dash.get_panel_group("imagespg")
project_images_gp.panels = ['images']


# Get Volumes gp and add [volumes, volumes_snapshot] panel
from openstack_dashboard.dashboards.project.volumes_snapshot import panel
project_volumes_gp = project_dash.get_panel_group("volumespg")
project_volumes_gp.panels = ['volumes', 'volumes_snapshot']
# remove snapshot tab in volumes panel
from openstack_dashboard.dashboards.project.volumes.tabs import SnapshotTab, VolumeAndSnapshotTabs, BackupsTab, VolumeTab
VolumeAndSnapshotTabs.tabs = (VolumeTab, BackupsTab)




project_security_gp = project_dash.get_panel_group("securitypg")
project_security_gp.panels = ['access_and_security']

"""for panel in project_compute_gp.panels:
	if panel=="overview":
		continue
	project_dash.unregister(project_dash.get_panel(panel).__class__)

from openstack_dashboard.dashboards.project.instances import panel
project_instances_gp = project_dash.get_panel_group("compute")
#project_dash.register('Instances')
project_instances_gp.panels.append('instances')
"""






# Change name of identity dashboard and set permission only admin
identity_dash = horizon.get_dashboard("identity")
identity_dash.name = "Manager Customer"
identity_dash.permissions = ('openstack.roles.admin',)


