#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules required for function

import requests
import json
import settings
import apicem
import time
import io

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()

class Command(apicem.Apicem):

    """APIC-EM command runner class"""

    def __init__(self):
        apicem.Apicem.__init__(self)

    def post_command(self):
        """
        Posts to Command runner a static request to a static device
        :param na: type string
        :return: Task ID
        """
        self.url = 'https://%s/api/v1/network-device-poller/cli/read-request ' % settings.apicIP
        self.data = json.dumps({"commands": ["show interface"],"deviceUuids": ["4602b8d7-6f58-4602-995e-4a531e7ea8c5"]})
        print self.data
        self.response_json = self.post_api(self.url, self.data)
        self.task_id = self.response_json['response']['taskId']
        return self.task_id


    def check_task_status(self, task_Id):
        """
        Posts to Command runner a static request to a static device
        :param task_Id: type string task_id field for the APIC-EM task API
        :return: File ID or Error Text
        """
        self.start_time = time.time()
        self.time_out = 45
        self.time = 0
        while (self.time < self.time_out):
            self.url = 'https://%s/api/v1/task/%s' % (settings.apicIP, task_Id)
            self.response_json = self.get_api(self.url)
            if self.response_json['response']['isError'] == False:
                if self.response_json['response']['progress'] != 'CLI Runner request creation':
                    return self.response_json['response']['progress']
            self.time = time.time() - self.start_time
        return 'Command runner Task timed out'

    def get_file(self, file_Id_dict):
        """
        Gets the text output from the file API
        :param task_Id: type string dictionary containing file id
        :return: json responce
        """
        #Probably should have used eval not json
        self.json_obj = file_Id_dict.replace("'", "\"")
        self.file_Id = json.loads(self.json_obj)
        self.file_Id = self.file_Id['fileId']
        self.url = 'https://%s/api/v1/file/%s' % (settings.apicIP, self.file_Id)
        self.response_json = self.get_api(self.url)
        return self.response_json
        