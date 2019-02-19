#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ChaosNetworkMonkey Console Script.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

# Import modules required for function

import requests
import json
import settings
import apicem
import random
import re
import urllib3
from pprint import pprint

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


__author__ = "Alan OReilly"
__email__ = "aoreilly@cisco.com"
__version__ = "0.1.1"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

class Template(apicem.Apicem):

    """Class for provide functions related to Templates including project and template getters and setters"""

    def __init__(self):
        apicem.Apicem.__init__(self)


    def get_project(self, proj_name):
        self.url = "https://%s/api/v1/template-programmer/project?name=%s" % (settings.dnacIP, proj_name)
        self.json_response = self.get_api(self.url)
        self.mydata = {}
        for i in self.json_response:
            self.mydata = {'projectName':i['name'], 'projectID':i['id'], 'templates': i['templates']}
        return self.mydata

    def get_template_id(self, project_id):
        self.url = "https://%s/api/v1/template-programmer/template/version/%s" % (settings.dnacIP, project_id)
        print self.url
        self.json_response = self.get_api(self.url)
        self.template_id = ''
        print 'hello'
        print self.json_response
        self.templates = {}
        for self.templates in self.json_response:
            print self.templates['versionsInfo']
            for self.ids in self.templates['versionsInfo']:
                print self.ids['id']
                self.templates = self.ids['id']
        return self.templates

    
    def create_project(self, proj_name):
        self.url = "https://%s/api/v1/template-programmer/project" % (settings.dnacIP)
        self.data = json.dumps({"name": proj_name, "tags": ['hello']})
        self.response_json = self.post_api(self.url, self.data)
        print ('Project Created %s' % proj_name)
        pass


    def create_template(self, project_id, template):
        self.url = "https://%s/api/v1/template-programmer/project/%s/template" % (settings.dnacIP, project_id)
        self.payload = template
        self.data = json.dumps(self.payload)
        self.response_json = self.post_api(self.url, self.data)
        pass


    def deploy_chaos_test(self, select_test, devices):
        print devices
        print select_test
        self.data = {
                    "forcePushTemplate": True,
                    "targetInfo": [devices],
                    "templateId": select_test
                    }

        #self.data = {'targetInfo':[{'params': {u'interface': u'gig1/0/22', u'vlan': u'20'},'type': 'MANAGED_DEVICE_IP', 'id': '10.10.22.66'}], 'forcePushTemplate': True, 'templateId': u'b248f640-5f48-487e-b735-77dd7f32743d'}            
        self.url = "https://%s/api/v1/template-programmer/template/deploy" % (settings.dnacIP)
        self.payload = json.dumps(self.data)
        #self.payload = self.data
        print self.payload
        self.response_json = self.post_api(self.url, self.payload)
        print self.response_json
        pass

