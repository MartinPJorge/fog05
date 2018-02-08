import sys
import os
sys.path.append(os.path.join(sys.path[0], 'interfaces'))
from fog05.interfaces.States import State
from fog05.interfaces.EntityInstance import EntityInstance
from jinja2 import Environment
import json


class KVMLibvirtEntityInstance(EntityInstance):

    def __init__(self, uuid, name, disk, cdrom, networks, user_file, ssh_key, entity_uuid, flavor_id, image_id):

        super(KVMLibvirtEntityInstance, self).__init__(uuid, entity_uuid)
        self.name = name
        self.disk = disk
        self.cdrom = cdrom
        self.networks = networks
        self.user_file = user_file
        self.ssh_key = ssh_key
        self.image_uuid = image_id
        self.flavor_uuid = flavor_id
        self.xml = None

    def on_configured(self, configuration):
        self.xml = configuration
        self.state = State.CONFIGURED

    def on_start(self):
        self.state = State.RUNNING
    
    def on_stop(self):
        self.state = State.CONFIGURED

    def on_pause(self):
        self.state = State.PAUSED

    def on_resume(self):
        self.state = State.RUNNING

    def on_clean(self):
        pass

    def before_migrate(self):
        pass

    def after_migrate(self):
        pass

