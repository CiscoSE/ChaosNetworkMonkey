#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules required for function

import requests
import json
import settings
import apicem
import resolveUser
import time

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


class Path(apicem.Apicem):

    """Class for provide functions related to path"""

    def __init__(self):
        apicem.Apicem.__init__(self)

    def get_users_ip(self, names):
        self.namelist = names.split()
        self.source_user_ip = resolveUser.resolveUser(self.namelist[2])
        self.dest_user_ip = resolveUser.resolveUser(self.namelist[3])
        return (self.source_user_ip, self.dest_user_ip)

    def submit_path(self, source, dest):
        self.url = 'https://%s/api/v1/flow-analysis' % settings.dnacIP
        self.data = json.dumps({'sourceIP': source, 'destIP': dest})
        self.response_json = self.post_api(self.url, self.data)
        self.flow_id = self.response_json['response']['flowAnalysisId']
        return self.flow_id

    def get_path(self, flow_id):
        self.url = 'https://%s/api/v1/flow-analysis/%s' \
            % (settings.dnacIP, flow_id)
        self.response_json = self.get_api(self.url)
        return self.response_json

    def format_path(self, path):
        self.message = ''
        if path['response']['networkElementsInfo']:
            self.message = 'Path Trace Complete ' + u'\u2705' + ' \n'
            for networkelements in path['response'
                    ]['networkElementsInfo']:
                if 'name' in networkelements:
                    self.message += '%s \n' % networkelements['name']
                    self.message += '       ' + u'\u25BC' + ' \n'
            self.message += 'Complete'
        else:
            self.message += 'Path trace incomplete\n'
            self.message += 'Status code: %s' % path['response'
                    ]['request']['status']
        return self.message

    def path_trace(self, names):
        (self.source, self.dest) = self.get_users_ip(names)
        self.flow_id = self.submit_path(self.source, self.dest)
        time.sleep(10)
        self.json_path = self.get_path(self.flow_id)
        self.message = self.format_path(self.json_path)
        return self.message


