from jsonschema import validate, ValidationError
from fog05 import Schemas
from enum import Enum
import re
import uuid
import json
import fnmatch
import time
import urllib3
import requests
from fog05 import API



class WebAPI(object):
    '''
        This class allow the interaction with fog05 using simple Python3 API
        Need the distributed store
    '''

    def __init__(self, sysid=0, store_id="python-api-rest"):

        self.api = API(store_id='fog05.rest')

        self.manifest = self.Manifest(self.api)
        self.node = self.Node(self.api)
        self.plugin = self.Plugin(self.api)
        self.network = self.Network(self.api)
        self.entity = self.Entity(self.api)
        self.image = self.Image(self.api)
        self.flavor = self.Flavor(self.api)

    def add(self, manifest):
        return self.api.add(manifest)

    def remove(self, entity_uuid):
        return self.api.remove(entity_uuid)

    class Manifest(object):
        '''
        This class encapsulates API for manifests

        '''
        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def check(self, manifest, manifest_type):
           return self.api.manifest.check(manifest, manifest_type)

        class Type(Enum):
            '''
            Manifest types
            '''
            ENTITY = 0
            IMAGE = 1
            FLAVOR = 3
            NETWORK = 4
            PLUGIN = 5

    class Node(object):
        '''

        This class encapsulates the command for Node interaction

        '''

        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def list(self):
            return self.api.node.list()

        def info(self, node_uuid):
            """
            Provide all information about a specific node

            :param node_uuid: the uuid of the node you want info
            :return: a dictionary with all information about the node
            """
            return self.api.node.info(node_uuid)

        def plugins(self, node_uuid):
            '''

            Get the list of plugin installed on the specified node

            :param node_uuid: the uuid of the node you want info
            :return: a list of the plugins installed in the node with detailed informations
            '''
            return self.api.node.plugins(node_uuid)

        def search(self, search_dict):
            '''

            Will search for a node that match information provided in the parameter

            :param search_dict: dictionary contains all information to match
            :return: a list of node matching the dictionary
            '''
            pass

    class Plugin(object):
        '''
        This class encapsulates the commands for Plugin interaction

        '''
        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def add(self, manifest, node_uuid=None):
            '''

            Add a plugin to a node or to all node in the system/tenant

            :param manifest: the dictionary representing the plugin manifes
            :param node_uuid: optional the node in which add the plugin
            :return: boolean
            '''
            if node_uuid is None:
                return self.api.plugin.add(manifest)
            else:
                return self.api.plugin.add(manifest,node_uuid)


        def remove(self, plugin_uuid, node_uuid=None):
            '''

            Will remove a plugin for a node or all nodes

            :param plugin_uuid: the plugin you want to remove
            :param node_uuid: optional the node that will remove the plugin
            :return: boolean
            '''
            pass

        def list(self, node_uuid=None):
            '''

            Same as API.Node.Plugins but can work for all node un the system, return a dictionary with key node uuid and value the plugin list

            :param node_uuid: can be none
            :return: dictionary {node_uuid, plugin list }
            '''
            if node_uuid is not None:
                return self.api.plugin.list(node_uuid)
            return self.api.plugin.list()



        def search(self, search_dict, node_uuid=None):
            '''

            Will search for a plugin matching the dictionary in a single node or in all nodes

            :param search_dict: dictionary contains all information to match
            :param node_uuid: optional node uuid in which search
            :return: a dictionary with {node_uuid, plugin uuid list} with matches
            '''
            pass

    class Network(object):
        '''

        This class encapsulates the command for Network element interaction

        '''

        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def add(self, manifest, node_uuid=None):
            '''

            Add a network element to a node o to all nodes


            :param manifest: dictionary representing the manifest of that network element
            :param node_uuid: optional the node uuid in which add the network element
            :return: boolean
            '''

            if node_uuid is not None:
                return self.api.network.add(manifest, node_uuid)
            return self.api.network.add(manifest)


        def remove(self, net_uuid, node_uuid=None):
            '''

            Remove a network element form one or all nodes

            :param net_uuid: uuid of the network you want to remove
            :param node_uuid: optional node from which remove the network element
            :return: boolean
            '''

            if node_uuid is not None:
               return self.api.network.remove(net_uuid,node_uuid)
            return self.api.network.remove(net_uuid)


        def list(self, node_uuid=None):
            '''

            List all network element available in the system/teneant or in a specified node

            :param node_uuid: optional node uuid
            :return: dictionary {node uuid: network element list}
            '''

            if node_uuid is not None:
               return self.api.network.list(node_uuid)
            return self.api.network.list(node_uuid)

        def search(self, search_dict, node_uuid=None):
            '''

            Will search for a network element matching the dictionary in a single node or in all nodes

            :param search_dict: dictionary contains all information to match
            :param node_uuid: optional node uuid in which search
            :return: a dictionary with {node_uuid, network element uuid list} with matches
            '''
            pass

    class Entity(object):
        '''

        This class encapsulates the api for interaction with entities

        '''

        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def define(self, manifest, node_uuid, wait=False):
            '''

            Defines an atomic entity in a node, this method will check the manifest before sending the definition to the node

            :param manifest: dictionary representing the atomic entity manifest
            :param node_uuid: destination node uuid
            :param wait: if wait that the definition is complete before returning
            :return: boolean
            '''
            return self.api.entity.define(manifest,node_uuid, wait)


        def undefine(self, entity_uuid, node_uuid, wait=False):
            '''

            This method undefine an atomic entity in a node

            :param entity_uuid: atomic entity you want to undefine
            :param node_uuid: destination node
            :param wait: if wait before returning that the entity is undefined
            :return: boolean
            '''
            return self.api.entity.undefine(entity_uuid, node_uuid, wait)

        def configure(self, entity_uuid, node_uuid, instance_uuid=None, wait=False):
            '''

            Configure an atomic entity, creation of the instance

            :param entity_uuid: entity you want to configure
            :param node_uuid: destination node
            :param instance_uuid: optional if preset will use that uuid for the atomic entity instance otherwise will generate a new one
            :param wait: optional wait before returning
            :return: intstance uuid or none in case of error
            '''
            if instance_uuid is None:
                instance_uuid = '{}'.format(uuid.uuid4())

            return self.api.entity.configure(entity_uuid, node_uuid, instance_uuid, wait)

        def clean(self, entity_uuid, node_uuid, instance_uuid, wait=False):
            '''

            Clean an atomic entity instance, this will destroy the instance

            :param entity_uuid: entity for which you want to clean an instance
            :param node_uuid: destionation node
            :param instance_uuid: instance you want to clean
            :param wait: optional wait before returning
            :return: boolean
            '''
            return self.api.entity.clean(entity_uuid, node_uuid, instance_uuid, wait)

        def run(self, entity_uuid, node_uuid, instance_uuid, wait=False):
            '''

            Starting and atomic entity instance

            :param entity_uuid: entity for which you want to run the instance
            :param node_uuid: destination node
            :param instance_uuid: instance you want to start
            :param wait: optional wait before returning
            :return: boolean
            '''
            return self.api.entity.run(entity_uuid, node_uuid, instance_uuid, wait)

        def stop(self, entity_uuid, node_uuid, instance_uuid, wait=False):
            '''

            Shutting down an atomic entity instance

            :param entity_uuid: entity for which you want to shutdown the instance
            :param node_uuid: destination node
            :param instance_uuid: instance you want to shutdown
            :param wait: optional wait before returning
            :return: boolean
            '''

            return self.api.entity.stop(entity_uuid, node_uuid, instance_uuid, wait)

        def pause(self, entity_uuid, node_uuid, instance_uuid, wait=False):
            '''

            Pause the exectution of an atomic entity instance

            :param entity_uuid: entity for which you want to pause the instance
            :param node_uuid: destination node
            :param instance_uuid: instance you want to pause
            :param wait: optional wait before returning
            :return: boolean
            '''
            return self.api.entity.pause(entity_uuid, node_uuid, instance_uuid, wait)

        def resume(self, entity_uuid, node_uuid, instance_uuid, wait=False):
            '''

            resume the exectution of an atomic entity instance

            :param entity_uuid: entity for which you want to resume the instance
            :param node_uuid: destination node
            :param instance_uuid: instance you want to resume
            :param wait: optional wait before returning
            :return: boolean
            '''

            return self.api.entity.resume(entity_uuid, node_uuid, instance_uuid, wait)

        def migrate(self, entity_uuid, instance_uuid, node_uuid, destination_node_uuid, wait=False):
            '''

            Live migrate an atomic entity instance between two nodes

            The migration is issued when this command is sended, there is a little overhead for the copy of the base image and the disk image


            :param entity_uuid: ntity for which you want to migrate the instance
            :param instance_uuid: instance you want to migrate
            :param node_uuid: source node for the instance
            :param destination_node_uuid: destination node for the instance
            :param wait: optional wait before returning
            :return: boolean
            '''

            return self.api.entity.migrate(entity_uuid, instance_uuid, node_uuid, destination_node_uuid, wait)

        def search(self, search_dict, node_uuid=None):
            pass

    class Image(object):
        '''

        This class encapsulates the action on images


        '''
        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def add(self, manifest, node_uuid=None):
            '''

            Adding an image to a node or to all nodes

            :param manifest: dictionary representing the manifest for the image
            :param node_uuid: optional node in which add the image
            :return: boolean
            '''
            if node_uuid is None:
                return self.api.image.add(manifest)
            return self.api.image.add(manifest, node_uuid)


        def remove(self, image_uuid, node_uuid=None):
            '''

            remove an image for a node or all nodes

            :param image_uuid: image you want to remove
            :param node_uuid: optional node from which remove the image
            :return: boolean
            '''

            if node_uuid is None:
                return self.api.image.remove(image_uuid)
            return self.api.image.remove(image_uuid, node_uuid)

        def search(self, search_dict, node_uuid=None):
            pass

    class Flavor(object):
        '''
          This class encapsulates the action on flavors

        '''
        def __init__(self, api=None):
            if api is None:
                raise RuntimeError('api cannot be none in API!')
            self.api = api

        def add(self, manifest, node_uuid=None):
            '''

            Add a computing flavor to a node or all nodes

            :param manifest: dictionary representing the manifest for the flavor
            :param node_uuid: optional node in which add the flavor
            :return: boolean
            '''

            if node_uuid is None:
                return self.api.flavor.add(manifest)
            return self.api.flavor.add(manifest,node_uuid)

        def remove(self, flavor_uuid, node_uuid=None):
            '''

            Remove a flavor from all nodes or a specified node

            :param flavor_uuid: flavor to remove
            :param node_uuid: optional node from which remove the flavor
            :return: boolean
            '''
            if node_uuid is None:
                return self.api.flavor.remove(flavor_uuid)
            return self.api.flavor.remove(flavor_uuid,node_uuid)

        def search(self, search_dict, node_uuid=None):
            pass

        def list(self, node_uuid=None):
            '''

            List all network element available in the system/teneant or in a specified node

            :param node_uuid: optional node uuid
            :return: dictionary {node uuid: network element list}
            '''
            if node_uuid is not None:
                return self.api.flavor.list(node_uuid)
            return self.api.flavor.list()
