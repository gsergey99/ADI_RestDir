#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pickle
import random
import binascii
from collections.abc import MutableMapping

import requests


def _marshall_(value):
    return binascii.b2a_base64(pickle.dumps(value))


def _unmarshall_(value):
    return pickle.loads(binascii.a2b_base64(value))


class RestDict(MutableMapping):

    def __init__(self, base_api_uri):
        self.uri = base_api_uri
        
        if self.uri.endswith('/'):
            self.uri = self.uri[:-1]
        
        result = requests.put(self.uri)

        if result.status_code not in [200, 201]:
            raise ValueError(f'Cannot create the dict: {result.status_code}')

    def keys(self):
        result = requests.get(f'{self.uri}/keys')
        if result.status_code != 200:
            raise ValueError(f'Cannot get keys, status code: {result.status_code}')
        try:
            result = json.loads(result.content.decode()).get('result', [])
        except Exception as error:
            raise ValueError(f'Cannot get keys: {error}')
        return result

    def delete_dict(self):
        result = requests.delete(f'{self.uri}')
        if result.status_code != 200:
            raise ValueError(f'Cannot delete restdict: {result.status_code} {self.uri}')

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(key)
        result = requests.get(f'{self.uri}/keys/{key}')
        if result.status_code == 404:
            raise KeyError(key)
        try:
    	    response = result.content.decode()
    	    response = json.loads(response)
    	    result = response['result']
        except Exception as error:
            raise ValueError(f'Cannot get item: {error}')
        try:
            return _unmarshall_(result)
        except Exception as error:
            raise ValueError(f'Unmarshalling error: {error}')

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(key)
        if key in self.keys():
            result = requests.post(f'{self.uri}/keys/{key}', data=_marshall_(value))
        else:
            result = requests.put(f'{self.uri}/keys/{key}', data=_marshall_(value))
        if result.status_code not in [200, 201]:
            raise ValueError(f'Cannot set item -> uri: {self.uri}/keys/{key}  code: {result.status_code}')

    def __delitem__(self, key):
        if not isinstance(key, str):
            raise TypeError(key)
        result = requests.delete(f'{self.uri}/keys/{key}')
        if result.status_code == 404:
            raise KeyError(key)
        if result.status_code != 204:
            raise RuntimeError(f'Cannot delete key: {result.status_code}')

    def _keytransform(self, key):
        return key