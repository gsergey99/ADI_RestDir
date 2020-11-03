#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Factories
'''

import urllib.parse
from restdict.client import RestDict
from restdict.server import DictServer


def new_server(server_address):
    '''
    Create new Web server with API REST
    '''
    return DictServer(server_address)


def new_restdict(server_api_uri, dict_name=None):
    '''
    Create new client connected to a given API URI
    '''
    return RestDict(server_api_uri)

def delete_restdict(server_api_uri, dict_name=None):

    
    test_dict = RestDict(server_api_uri)

    test_dict.__delitem__(dict_name)
    
    

def connect_restdict(server_api_uri, dict_name=None):

    return RestDict(server_api_uri)[dict_name]