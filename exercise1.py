import keystoneclient.v2_0.client as keystone
import glanceclient as glance
import novaclient.v1_1.client as nova
import os

from credentials import get_keystone_creds
from credentials import get_nova_creds

if __name__ == '__main__':
    keystoneInfo = get_keystone_creds()
    novaInfo = get_nova_creds()
    keystoneclient = keystone.Client(**keystoneInfo)
    novaclient = nova.Client(**novaInfo)
    
    endPoint = keystoneclient.service_catalog.get_urls(service_type = 'image')[0]
    glanceclient = glance.Client('1', endPoint, token = keystoneclient.auth_token)
    
    images = glanceclient.images.list()
    image_create = None
    for image in images:
        if image.name.find('ubuntu') > -1:
            print image.id, '\t', image.name
            flavor = novaclient.flavors.find(name="m1.micro")
            instance = novaclient.servers.create(name=image.id, image=image, flavor=flavor)
            