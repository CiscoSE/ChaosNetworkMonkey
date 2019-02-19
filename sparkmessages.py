#!/usr/bin/python
# -*- coding: utf-8 -*-

# import the requests library so we can use it to make REST calls

import requests
import json
import settings
import ssl

# disable warnings about using certificate verification

requests.packages.urllib3.disable_warnings()


class Message:

    """ Spark Message logicLogic """

    def __INIT__(self):
        self.token = ''

    def get_message(self, message_id):

        # login to developer.ciscospark.com and copy your access token here
        # Never hard-code access token in production environment

        self.token = settings.apic_sparkToken

        # add authorization to the header

        self.header = {'Authorization': '%s' % self.token}

        # create request url using message ID

        self.get_rooms_url = 'https://api.ciscospark.com/v1/messages/' \
            + message_id

        # send the GET request and do not verify SSL certificate for simplicity of this example

        self.api_response = requests.get(self.get_rooms_url,
                headers=self.header, verify=False)

        # parse the response in json

        self.response_json = self.api_response.json()

        # get the text value from the response

        self.text = self.response_json['text']
        
        # get the email of the sender

        self.sender = self.response_json['personEmail']

        # return the text value

        return (self.text, self.sender)

    def post_message(
        self,
        person_id,
        person_email,
        room_id,
        text,
        ):

        # define a variable for the hostname of Spark

        self.hostname = settings.spark_hostname

        # login to developer.ciscospark.com and copy your access token here
        # Never hard-code access token in production environment

        self.token = settings.apic_sparkToken

        # add authorization to the header

        self.header = {'Authorization': '%s' % self.token,
                       'content-type': 'application/json'}

        # specify request url

        self.post_message_url = 'https://api.ciscospark.com/v1/messages'

        # create message in Spark room

        self.payload = {
            'personId': person_id,
            'personEmail': person_email,
            'roomId': room_id,
            'text': text,
            }

        # create POST request do not verify SSL certificate for simplicity of this example

        self.api_response = requests.post(self.post_message_url,
                json=self.payload, headers=self.header, verify=False)

        # get the response status code

        self.response_status = self.api_response.status_code

        # return the text value

        print self.response_status