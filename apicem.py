#!/usr/bin/python
# -*- coding: utf-8 -*-

# Import modules required for function

import requests
import json
import settings
import ssl
import base64
from requests.auth import HTTPBasicAuth

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


class Apicem:

    """Base class for APICEM related functions """

    token = ''

    def __init__(self):
        Apicem.token = self.get_token()

    def get_token(self):
        dnacBase = settings.dnacIP
        dnacUser = settings.dnacUser
        dnacPass = settings.dnacPass
        #payload = {'username': dnacUser, 'password': dnacPass}
        
        # HTTP Basic Authentication code below for illustration purposes only
        # Note: the below is to accommodate different syntax in Python 2 vs 3:
        try:
            DNAC_CREDENTIALS = bytes(dnacUser+':'+dnacPass)
        except:
            DNAC_CREDENTIALS = bytes(dnacUser+':'+dnacPass, 'utf-8')

        DNAC_B64 = (base64.b64encode(DNAC_CREDENTIALS)).decode('utf-8')
        DNAC_AUTH_HEADERS = {
            'authorization' : 'Basic ' + DNAC_B64,
            'content-type'  : 'application/json'
        }

        url = 'https://%s/api/system/v1/auth/token' % dnacBase

        # Content type must be included in the header

        #header = {'content-type': 'application/json'}

        # Format the payload to JSON and add to the data.  Include the header in the call.
        # SSL certification is turned off, but should be active in production environments

        #response = requests.post(url, data=json.dumps(payload),
        #                         headers=header, verify=False)

        response = requests.post(url=url, auth=HTTPBasicAuth(dnacUser,dnacPass), verify=False)

        # Check if a response was received. If not, print an error message.

        if not response:
            print 'Could not get login ticket, No data returned!'
        else:

            # Data received.  Get the ticket and return.
            self.token = response.json()['Token']
        return self.token

    def get_api(self, url):
        if Apicem.token:
            token = Apicem.token
            self.headerInfo = {'X-Auth-Token': token}
            self.response = requests.get(url, headers=self.headerInfo,
                    verify=False)
            self.jsonresponse = self.response.json()
            return self.jsonresponse
        else:
            print 'Issue with DNAC Auth Token'

    def post_api(self, url, payload):
        if Apicem.token:
            token = Apicem.token
            self.header = {'Content-type': 'application/json',
                           'X-Auth-Token': token}
            self.response = requests.post(url, data=payload,
                    verify=False, headers=self.header)
            self.jsonresponse = self.response.json()
            return self.jsonresponse
        else:
            print 'Issue with DNAC Auth Token'


