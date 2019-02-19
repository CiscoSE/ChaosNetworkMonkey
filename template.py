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


class Template(apicem.Apicem):

    """Class for provide functions related to Templates including project and template getters and setters"""

    def __init__(self):
        apicem.Apicem.__init__(self)


