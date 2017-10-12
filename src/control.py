from interfaces.Agent import Agent
from PluginLoader import PluginLoader
import uuid
import sys
from DStore import *
# from RedisLocalCache import RedisCache
import json


class Controll():
    def __init__(self):
        self.uuid = uuid.uuid4()
        sid = str(self.uuid)
        self.root = "fos://<sys-id>"
        self.home = str("fos://<sys-id>/%s" % sid)
        self.nodes = {}
        # Notice that a node may have multiple caches, but here we are
        # giving the same id to the nodew and the cache
        self.store = DStore(sid, self.root, self.home, 1024)

    def nodeDiscovered(self, uri, value, v = None):
        value = json.loads(value)
        if uri != str('fos://<sys-id>/%s/' % self.uuid):
            print ("###########################")
            print ("###########################")
            print ("### New Node discovered ###")
            print ("UUID: %s" % value.get('uuid'))
            print ("Name: %s" % value.get('name'))
            print ("###########################")
            print ("###########################")
            self.nodes.update({ len(self.nodes)+1 : {value.get('uuid'): value}})



    def show_nodes(self):
        for k in self.nodes.keys():
            n = self.nodes.get(k)
            id = list(n.keys())[0]
            print ("%d - %s : %s" % (k, n.get(id).get('name'), id))



    def main(self):


        uri = str('fos://<sys-id>/*/')
        self.store.observe(uri, self.nodeDiscovered)



        while len(self.nodes) == 0:
            time.sleep(2)


        self.show_nodes()

        n = int(input("Select node: "))

        node_uuid = self.nodes.get(n)
        if node_uuid is not None:
            node_uuid = list(node_uuid.keys())[0]
            if node_uuid is not None:
                pass
        else:
            exit()

        uri = str('fos://<sys-id>/%s/plugins' % node_uuid)
        all_plugins = json.loads(self.store.get(uri)).get('plugins')

        runtimes = [x for x in all_plugins if x.get('type') == 'runtime']
        print("locating kvm plugin")
        kvm = [x for x in runtimes if 'kvm' in x.get('name')][0]


        vm_uuid = str(uuid.uuid4())

        vm_name = 'test'

        vm_definition = {'name': vm_name, 'uuid': vm_uuid, 'cpu': 1, 'memory': 128, 'disk_size': 5, 'base_image':
                            'http://download.cirros-cloud.net/0.3.5/cirros-0.3.5-x86_64-disk.img'}

        entity_definition = {'status': 'define', 'name': vm_name, 'version': 1, 'entity_data': vm_definition}


        json_data = json.dumps(entity_definition)

        print("Press enter to define a vm")
        input()

        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s' % (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.put(uri, json_data)

        print("Press enter to configure the vm")
        input()

        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s#status=configure' %
                  (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.dput(uri)

        print("Press enter to start vm")
        input()

        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s#status=run' % (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.dput(uri)

        print("Press enter to stop vm")
        input()

        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s#status=stop' % (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.dput(uri)

        print("Press enter to clean the vm")
        input()

        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s#status=clean' %
                  (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.dput(uri)

        print("Press enter to undefine the vm")
        input()

        json_data = json.dumps({'status': 'undefine'})
        uri = str('fos://<sys-id>/%s/runtime/%s/entity/%s' %
                  (node_uuid, kvm.get('uuid'), vm_uuid))
        self.store.dput(uri, json_data)



        input()

        exit(0)


if __name__ == '__main__':
    c = Controll()
    c.main()