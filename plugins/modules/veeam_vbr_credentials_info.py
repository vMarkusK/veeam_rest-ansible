#!/usr/bin/env python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: veeam_vbr_credentials_info

short_description: 

version_added: "1.0.0"

description: 

options:
    server_name:
        description: VBR Server Name or IP
        required: true
        type: str
    server_port:
        description: VBR RestAPI Sever Port
        required: false
        default: 9419
        type: str
    server_username:
        description: VBR Server Username
        required: true
        type: str
    server_password:
        description: VBR Server password
        required: true
        type: str
    validate_certs:
        description: SSL Certificate Validation
        required: false
        default: false
        type: bool

author:
    - Markus Kraus (@vMarkusK)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
  - name: Test veeam_vbr_credentials_info
    veeamhub.veeam_rest.veeam_vbr_credentials_info:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
    register: testout
  - name: Debug Result
    debug:
        var: testout
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
"msg": {
        "data": [
            {
                "SSHPort": 22,
                "addToSudoers": false,
                "autoElevated": false,
                "creationDateTime": "06.10.2020 20:05:57",
                "description": "Helper appliance credentials",
                "id": "70275b03-e805-49e1-9535-1867c62371e2",
                "passphrase": "",
                "privateKey": "",
                "tag": "70275B03-E805-49E1-9535-1867C62371E2",
                "type": "Linux",
                "useSu": false,
                "username": "root"
            },
            {
                "creationDateTime": "06.10.2020 18:05:22",
                "description": "Tenant-side network extension appliance credentials",
                "id": "b5ebaf50-1a63-4c48-839f-5f8a5452520b",
                "tag": "B5EBAF50-1A63-4C48-839F-5F8A5452520B",
                "type": "Standard",
                "username": "root"
            },
            {
                "creationDateTime": "06.10.2020 18:05:32",
                "description": "Azure helper appliance credentials",
                "id": "e379ded2-8dae-4b9a-b77d-7ed99e8c7152",
                "tag": "E379DED2-8DAE-4B9A-B77D-7ED99E8C7152",
                "type": "Standard",
                "username": "root"
            },
            {
                "creationDateTime": "06.10.2020 18:05:22",
                "description": "Provider-side network extension appliance credentials",
                "id": "fd0041d1-4a68-4abd-aefe-b2bf02bb7ca9",
                "tag": "FD0041D1-4A68-4ABD-AEFE-B2BF02BB7CA9",
                "type": "Standard",
                "username": "root"
            }
        ],
        "pagination": {
            "total": 0
        }
    }
'''

import json
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=True),
        server_username=dict(type='str', required=True),
        server_password=dict(type='str', required=True, no_log=True),
        server_port=dict(type='str', default='9419'),
        validate_certs=dict(type='bool', default='no'),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
        )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    ## Authenticate
    request_server = module.params['server_name']
    request_port = module.params['server_port']
    request_username = module.params['server_username']
    request_password = module.params['server_password']
    payload = 'grant_type=password&username=' + request_username + '&password=' + request_password
    headers = {
        'accept': 'application/json',
        'x-api-version': '1.0-rev1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'true'
        }

    request_url = 'https://' + request_server + ':' + request_port + '/api/oauth2/token'

    method = "Post"
    req, info = fetch_url(module, request_url, headers=headers, method=method, data=payload)

    resp = json.loads(req.read())

    headers = {
        'x-api-version': '1.0-rev1',
        'Authorization': 'Bearer ' + resp['access_token']
        }
    request_url = 'https://' + request_server + ':' + request_port + '/api/v1/credentials'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    result['msg'] = json.loads(req.read())
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()