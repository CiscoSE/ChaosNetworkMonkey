#!/usr/bin/python
# -*- coding: utf-8 -*-

from SOAPpy import SOAPProxy
import sys
import settings
import requests

__INSTANCE__ = settings.servicenow_instance

sparkHostName = settings.spark_hostname
sparkToken = settings.sn_sparkToken
personId = settings.sn_personId
personEmail = settings.sn_personEmail
roomId = settings.roomId


def createincident(params_dict):
    instance = __INSTANCE__
    username = settings.servicenow_username
    password = settings.servicenow_password
    proxy = 'https://%s:%s@%s.service-now.com/incident.do?SOAP' \
        % (username, password, instance)
    namespace = 'http://www.service-now.com/'
    server = SOAPProxy(proxy, namespace)
    response = server.insert(
        impact=int(params_dict['impact']),
        urgency=int(params_dict['urgency']),
        priority=int(params_dict['priority']),
        category=params_dict['category'],
        location=params_dict['location'],
        caller_id=params_dict['user'],
        assignment_group=params_dict['assignment_group'],
        assigned_to=params_dict['assigned_to'],
        short_description=params_dict['short_description'],
        comments=params_dict['comments'],
        )
    return response
    
def add_comment(sys_id):
    instance = __INSTANCE__
    url = 'https://%s.service-now.com/api/now/table/incident/%s' % (instance, sys_id)

    # Eg. User name="admin", Password="admin" for this code sample.
    user = settings.servicenow_username
    pwd = settings.servicenow_password

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.put(url, auth=(user, pwd), headers=headers ,data=" {'comments':'User is connected to Network Host IP: 212.1.10.20, Host Mac: 5c:f9:dd:52:07:78'}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    
def add_comment2(sys_id):
    instance = __INSTANCE__
    url = 'https://%s.service-now.com/api/now/table/incident/%s' % (instance, sys_id)

    # Eg. User name="admin", Password="admin" for this code sample.
    user = settings.servicenow_username
    pwd = settings.servicenow_password

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.put(url, auth=(user, pwd), headers=headers ,data=" {'comments':'Connected to device: CAMPUS-Access1 on port: GigabitEthernet1/0/47 '}")

    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)


def get_user_location(user):
    location = ''
    if user == 'Alice':
        location = 'Bedfont'
    elif user == 'Bob':
        location = 'London City'
    return location


# TODO Get message that were already sent by APIC-EM

def get_previous_message(message_num):
    return None


# Post URL into Spark Room

def post_message_spark(incident_sysid):
    message = ''

    # https://dev21113.service-now.com/nav_to.do?uri=incident.do?sys_id=c80c88ccdb9e120027d9f001cf961927

    if incident_sysid['sys_id']:
        sysid = incident_sysid['sys_id']
        url = \
            'https://%s.service-now.com/nav_to.do?uri=incident.do?sys_id=%s' \
            % (__INSTANCE__, sysid)
        try:
            post_message_url = 'https://%s/v1/messages' % sparkHostName

            header = {'Authorization': '%s' % sparkToken,
                      'content-type': 'application/json'}

            payload = {
                'personId': personId,
                'personEmail': personEmail,
                'roomId': roomId,
                'text': 'Raised Case %s' % url,
                }

            api_response = requests.post(post_message_url,
                    json=payload, headers=header, verify=False)
            response_status = api_response.status_code
            print response_status
        except:
            print 'Could not update Spark'
    else:
        message = 'Could not create case'
    return None


def raise_case(spark_text):
    print 'trying to raise case'
    splitted = spark_text.split()
    comment = spark_text.split(' ', 1)[1]
    comment = comment.split(' ', 1)[1]
    comment = comment.split(' ', 1)[1]
    values = {
        'impact': '2',
        'urgency': splitted[2],
        'priority': '3',
        'category': 'Network',
        'location': 'Bedfont',
        'user': splitted[1],
        'assignment_group': 'Technical Support',
        'assigned_to': 'Fred Luddy',
        'short_description': comment,
        'comments': 'Case raised via Cisco Spark'
        }
    print values
    new_incident_sysid = createincident(values)
    print 'Returned sysid: ' + repr(new_incident_sysid)
    print new_incident_sysid
    sys_id = new_incident_sysid['sys_id']
    print '\n\nSys-ID:%s' % sys_id
    message = post_message_spark(new_incident_sysid)
    add_comment(sys_id)
    add_comment2(sys_id)


values = {
    'impact': '1',
    'urgency': '2',
    'priority': '3',
    'category': 'Network',
    'location': 'Bedfont',
    'user': 'alice@cisco.local',
    'assignment_group': 'Technical Support',
    'assigned_to': 'Fred Luddy',
    'short_description': 'User having issues connecting to Network',
    'comments': 'Case raised via Cisco Spark',
    }
