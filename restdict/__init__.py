#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    Factories
'''

import urllib.parse
from restdict.client import RestDict
from restdict.server import DictServer
import uuid

DICT = {}

def new_server(server_address):
    '''
    Create new Web server with API REST
    '''
    return DictServer(server_address)


def new_restdict(server_api_uri, dict_name=None):
    
    if dict_name is None:
        dict_name = str(uuid.uuid4())
    
    compl_uri = f'{server_api_uri}/{dict_name}'
    DICT[compl_uri] = RestDict(compl_uri)
    
    return DICT[compl_uri]

def connect_restdict(server_api_uri, dict_name):

    compl_uri = f'{server_api_uri}/{dict_name}'

    if compl_uri not in DICT:
        raise Exception

    return DICT[compl_uri]


def delete_restdict(server_api_uri, dict_name):

    compl_uri = f'{server_api_uri}/{dict_name}'

    if compl_uri not in DICT:
        raise Exception

    DICT[compl_uri].delete_dict()

    del DICT[compl_uri]