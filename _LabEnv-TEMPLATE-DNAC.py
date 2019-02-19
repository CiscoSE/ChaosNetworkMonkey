#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2018 Bruno Klauser <bklauser@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ''AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#
# TECHNICAL ASSISTANCE CENTER (TAC) SUPPORT IS NOT AVAILABLE FOR THIS SCRIPT.
# ############################################################################
#
# This script contains a set of shared environment definitions
#
# ############################################################################
import base64
import json
import requests
import sys
# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

# Replace YOUR-NAME-HERE in the line below
LAB_USER = 'a dedicated Blackbelt'

# Get your Cisco Spark access token from developer.ciscospark.com
# 1) Login
# 2) Copy the Access Token from top-right corner portrait icon
# 3) replace YOUR-ACCESS-TOKEN-HERE in the line below
LAB_USER_SPARK_TOKEN = 'YOUR-ACCESS-TOKEN-HERE'

LAB_SESSION = '5th Blackbelt Summit'

# SPARK_TEAM_NAME = 'private-TEST'
SPARK_TEAM_NAME = 'Cisco EMEAR DNA Programmability and Automation'
# SPARK_TEAM_NAME = None
SPARK_ROOM_NAME = 'Blackbelt Scripts and Bots'

# ############################################################################
# Do not edit below this line, unless instructed to do so
# ############################################################################
SPARK_ROOM_ID = None
SPARK_TEAM_ID = None

SPARK_TOKEN = 'Bearer '+LAB_USER_SPARK_TOKEN
SPARK_HEADERS = {
  'Content-type': 'application/json',
  'Authorization': SPARK_TOKEN
}

SPARK_API = 'https://api.ciscospark.com/v1'
SPARK_API_MESSAGES = '%s/messages' % SPARK_API
SPARK_API_ROOMS = '%s/rooms' % SPARK_API
SPARK_API_TEAMS = '%s/teams' % SPARK_API
SPARK_API_MEMBERS = '%s/team/memberships' % SPARK_API

DNAC_USR = 'devnetuser'
DNAC_PWD = 'Cisco123!'
DNAC_HOST = 'sandboxdnac.cisco.com'

DNAC_API = 'https://%s/api/v1' % DNAC_HOST
DNAC_AUTH_API = 'https://%s/api/system/v1/auth/login' % DNAC_HOST
DNAC_HEADERS = {'Content-type': 'application/json'}

# HTTP Basic Authentication code below for illustration purposes only
# Note: the below is to accommodate different syntax in Python 2 vs 3:
try:
  DNAC_CREDENTIALS = bytes(DNAC_USR+':'+DNAC_PWD)
except:
  DNAC_CREDENTIALS = bytes(DNAC_USR+':'+DNAC_PWD, 'utf-8')

DNAC_B64 = (base64.b64encode(DNAC_CREDENTIALS)).decode('utf-8')
DNAC_AUTH_HEADERS = {
  'authorization' : 'Basic ' + DNAC_B64,
  'content-type'  : 'application/json'
}


# ############################################################################
# Utiliy Function to find and post a message into SPARK_ROOM_NAME
# ############################################################################
def postSparkMessage(tmp_message):
    global SPARK_ROOM_ID
    global SPARK_TEAM_ID

    if SPARK_TEAM_NAME is None:
      if SPARK_ROOM_ID is None:
        r = requests.get(SPARK_API_ROOMS, headers=SPARK_HEADERS, verify=False)
        j = json.loads(r.text)

        for tmproom in j['items']:
          if tmproom['title'] == SPARK_ROOM_NAME:
            SPARK_ROOM_ID = tmproom['id']
            print("Found room ID for '" + SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
            break

        if SPARK_ROOM_ID is None:
          print("Failed to find room ID for '" + SPARK_ROOM_NAME + "'")
          return None

      m = json.dumps({'roomId':SPARK_ROOM_ID,'markdown':tmp_message})
      r = requests.post(SPARK_API_MESSAGES, data=m, headers=SPARK_HEADERS, verify=False)
      return r

    else:
      if SPARK_TEAM_ID is None:
        r = requests.get(SPARK_API_TEAMS, headers=SPARK_HEADERS, verify=False)
        j = json.loads(r.text)
        for tmpteam in j['items']:
          if tmpteam['name'] == SPARK_TEAM_NAME:
            SPARK_TEAM_ID = tmpteam['id']
            break

        if SPARK_TEAM_ID is None:
          print("==> Failed to find team ID for '" + SPARK_TEAM_NAME + "'")
          sys.exit(1)

      if SPARK_ROOM_ID is None:
        m = 'teamId='+SPARK_TEAM_ID
        r = requests.get(SPARK_API_ROOMS, params=m, headers=SPARK_HEADERS, verify=False)
        j = json.loads(r.text)
        for tmproom in j['items']:
          if tmproom['title'] == SPARK_ROOM_NAME:
            SPARK_ROOM_ID = tmproom['id']
            print("Found room ID for '" + SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
            break

        if SPARK_ROOM_ID is None:
          print("Failed to find room ID for '" + SPARK_ROOM_NAME + "'")
          return None

      m = json.dumps({'roomId':SPARK_ROOM_ID,'markdown':tmp_message})
      r = requests.post(SPARK_API_MESSAGES, data=m, headers=SPARK_HEADERS, verify=False)
      return r

# ############################################################################
# EOF
# ############################################################################
