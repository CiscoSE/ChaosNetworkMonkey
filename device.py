#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules required for function

import requests
import json
import settings
import apicem
import random
import re

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


class Device(apicem.Apicem):

    """DNAC network device class"""

    def __init__(self):
        apicem.Apicem.__init__(self)

    def list_all_devices(self):
        self.url = 'https://%s/api/v1/network-device' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        self.result = ''
        if self.json_response:
            for device in self.json_response['response']:
                #self.result += device['hostname'] + '\n'
                print device
            return self.result
        return False

    def get_all_devices(self):    
        self.url = 'https://%s/api/v1/network-device' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        return self.json_response

    def resolve_device_name(self, device_name):
        self.url = 'https://%s/api/v1/network-device' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        if self.json_response:
            for device in self.json_response['response']:
                if device['hostname'] == device_name:
                    return device['id']
        return False
    
    def resolve_device_id(self, device_id):
        self.url = 'https://%s/api/v1/network-device/%s' \
            % (settings.dnacIP, device_id)
        self.json_response = self.get_api(self.url)
        return self.json_response['response']['hostname']

    def format_get_health_all(self, devices):
        self.total = devices['Reachable'] + devices['Unreachable'] \
            + devices['Unknown']
        self.message = 'Total Number of Devices: %s \n' % self.total
        if devices['Reachable'] != 0:
            self.message += 'Number of reachable devices: %s ' \
                % devices['Reachable'] + u'\u2705' + '\n'
        if devices['Reachable'] != 0:
            self.message += 'Number of unreachable devices: %s ' \
                % devices['Unreachable'] + u'\u274E' + '\n'
        if devices['Unknown'] != 0:
            self.message += 'Number of unknown devices: %s ' \
                % devices['Unknown'] + u'\u2753' + '\n'
        return self.message

    def get_health_all(self):
        self.url = 'https://%s/api/v1/network-device' % settings.dnacIP
        self.devices = {'Reachable': 0, 'Unreachable': 0, 'Unknown': 0}
        self.message = ''
        self.json_response = self.get_api(self.url)
        for device in self.json_response['response']:
            if device['reachabilityStatus'] == 'Reachable':
                self.devices['Reachable'] += 1
            elif device['reachabilityStatus'] == 'Unreachable':
                self.devices['Unreachable'] += 1
            else:
                self.devices['Unknown'] += 1
        return self.format_get_health_all(self.devices)

    def get_health_device(self):
        pass

    def device_count(self):
        self.url = 'https://%s/api/v1/network-device/count' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        return self.json_response['response']    

    def check_location(self, location):
        self.url = 'https://%s/api/v1/location' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        for locations in self.json_response['response']:
            if locations['locationName'] == location:
                return locations['id']
        return False

    def get_devices_location(self, location):
        self.message = ''
        self.locationid = self.check_location(location)
        self.url = 'https://%s/api/v1/network-device/location/%s' \
            % (settings.dnacIP, self.locationid)
        self.json_response = self.get_api(self.url)
        if self.json_response['response']:
            for devices in self.json_response['response']:
                self.message += '%s \n' % devices['hostname']
        else:
            self.message = 'No devices found in this location'
        return self.message

    def get_random_device_id_host(self):
        self.device_count_int = ''
        self.response = ''
        self.device_count_int = self.device_count()
        self.rnd = random.randint(1, self.device_count_int)
        self.response = self.get_all_devices()
        self.device_counter = 1
        for device in self.response['response']:
            if self.rnd == self.device_counter:
                self.device_id = (device['id'])
                self.device_hostname = (device['hostname'])
                print (self.device_hostname)
                #self.device_output = {'id':self.device_id, 'hostName':self.device_hostname, "type": "MANAGED_DEVICE_IP" }
                #self.device_output = {'id':self.device_id, "type": "MANAGED_DEVICE_IP" }
                self.device_output = {'id':'10.10.22.66', "type": "MANAGED_DEVICE_IP" }    
            self.device_counter = self.device_counter + 1
        return self.device_output

    def get_random_device_id_host(self):
        self.device_count_int = ''
        self.response = ''
        self.device_count_int = self.device_count()
        self.rnd = random.randint(1, self.device_count_int)
        self.response = self.get_all_devices()
        self.device_counter = 1
        for device in self.response['response']:
            if self.rnd == self.device_counter:
                self.device_ip = (device['managementIpAddress'])
                self.device_hostname = (device['hostname'])
                print (self.device_hostname)
                self.device_output = {'id': self.device_ip, "type": "MANAGED_DEVICE_IP" }    
            self.device_counter = self.device_counter + 1
        return self.device_output