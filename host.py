#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules required for function

import requests
import json
import settings
import apicem
import resolveUser
import device

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


class Host(apicem.Apicem):

    def __init__(self):
        apicem.Apicem.__init__(self)

    def get_all_hosts(self):
        self.url = 'https://%s/api/v1/host' % settings.dnacIP
        self.response_json = self.get_api(self.url)
        self.message = ''
        if self.response_json:
            for host in self.response_json['response']:
                self.message += '[Host IP: ' + host['hostIp'] \
                    + ', Host Mac: ' + host['hostMac'] + '] \n'
            return self.message
        else:
            return self.message

    def get_individual_host(self, name):
        self.ip = resolveUser.resolveUser(name)
        self.url = 'https://%s/api/v1/host?hostIp=%s' \
            % (settings.dnacIP, self.ip)
        self.response_json = self.get_api(self.url)
        self.message = ''
        for host in self.response_json['response']:
            #print host
            self.message += 'User is connected to Network ' + u'\u2705' \
                + ' \n'
            self.message += '[Host IP: ' + host['hostIp'] \
                + ', Host Mac: ' + host['hostMac'] + '] \n'
            try:
                apic_device = device.Device()
                self.connected_device = \
                    apic_device.resolve_device_id(host['connectedNetworkDeviceId'
                        ])
                del apic_device
                self.message += 'Connected to device: %s \n' \
                    % self.connected_device
                if host['connectedInterfaceName']:    
                    self.message += 'Connected to port: %s \n' \
                    % host['connectedInterfaceName']
                if host['vlanId']:
                    self.message += 'Connected to vlan: %s \n' \
                    % host['vlanId']
                else:
                    self.message += ' '           
            except:
                print "No Attached Device"
        return self.message

    def get_connected_host(self, device_name):
        self.message = ''
        self.device_id = ''
        self.url = 'https://%s/api/v1/network-device' % settings.dnacIP
        self.json_response = self.get_api(self.url)
        for device in self.json_response['response']:
            if device['hostname'] == device_name:
                self.device_id = device['id']
        if self.device_id:
            self.url = 'https://%s/api/v1/host' % settings.dnacIP
            self.response_json = self.get_api(self.url)
            for host in self.response_json['response']:
                if host['connectedNetworkDeviceId'] == self.device_id:
                    self.message += '[Host IP: ' + host['hostIp'] \
                        + ', Host Mac: ' + host['hostMac'] + '] \n'
            return self.message

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
        for devices in self.json_response['response']:
            self.message += '%s \n' % devices['hostname']
        return self.message

    def get_host_location(self, location):
        self.location_id = self.check_location(location)


