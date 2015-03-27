import keystoneclient
import keystoneclient.v2_0.client as ksclient
from config import *


def get_client():
	"""
	"""
	keystone = ksclient.Client(auth_url=END_POINT, username=USERNAME, password=PASSWORD, tenant_name=PROJECT_NAME)
	return keystone

def _create_project(name, description=None, keystone=None):
	if not keystone:
		keystone = get_client()
	project = keystone.tenants.create(tenant_name=name,
                        description=description,
                        enabled=True)
	return project

def _create_user(name, project_id, password,
                        email=None, enabled=None, keystone=None):
	"""
	"""
	if not keystone:
		keystone = get_client()
	user = keystone.users.create(name, tenant_id=project_id, password=password, 
			email=email, enabled=enabled)
	return user

def create_user(name, password, email=None, description=None, enabled=False):
	"""
	"""
	keystone = get_client()
	try:
    		project = _create_project(name, description, keystone)
	except keystoneclient.openstack.common.apiclient.exceptions.Conflict:
		raise Exception("User already exist") 
	role = keystone.roles.create(name)
	try:
		user = _create_user(name, project_id=project.id, password=password, 
			email=email, enabled=enabled, keystone=keystone)
	except keystoneclient.openstack.common.apiclient.exceptions.Conflict:
		raise Exception("User already exist")
	keystone.roles.add_user_role(user, role, project)
	return user

def enable_user(user_id, keystone=None):
	"""
	"""
        if not keystone:
                keystone = get_client()
	user = keystone.users.update(user=user_id, enabled=True)	
	return user

