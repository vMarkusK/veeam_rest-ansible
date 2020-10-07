#!/usr/bin/env python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: veeam_vbr_credentials

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
    type:
        description:
        - Set to C(Windows) to create new windows credentials.
        - Set to C(Linux) to create new liniux credentials.
        - Set to C(Standard) to create new standard credentials.
        type: str
        choices: [ windows, linux, standard ]
        default: standard

author:
    - Markus Kraus (@vMarkusK)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
  - name: Test veeam_vbr_credentials Create
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
        type: 'Linux'
        username: ''
        password: '<Password>'
        description: 'Created by Ansible RestAPI Module'
    register: testout
  - name: Debug Result
    debug:
        var: testout
  - name: Test veeam_vbr_credentials_info
    veeamhub.veeam_rest.veeam_vbr_credentials_info:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
    register: testout
  - name: Debug Result
    debug:
        var: testout
  - name: Test veeam_vbr_credentials Delete
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
        id: '0b3f7851-a809-4731-989f-9f08820f4be6'
        state: absent
    register: testout
  - name: Debug Result
    debug:
        var: testout
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
        "SSHPort": 22,
        "addToSudoers": false,
        "autoElevated": false,
        "creationDateTime": "07.10.2020 00:08:45",
        "description": "Created by Ansible RestAPI Module",
        "id": "317da5a8-3d12-428b-b1d7-95e9e780bb14",
        "passphrase": "",
        "privateKey": "",
        "tag": "6b8ced39-4e37-4b95-8e8c-8179a3dcfab5",
        "type": "Linux",
        "useSu": false,
        "username": "root"
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
        state = dict(type = "str", choices = ("absent", "present"), default = "present" ),
        id=dict(type='str', required=False),
        username=dict(type='str', required=False),
        password=dict(type='str', required=False, no_log=True),
        type=dict(type='str', choices=("Windows", "Linux", "Standard"), default='Standard'),
        description=dict(type='str', required=False),
        tag=dict(type='str', required=False),
        validate_certs=dict(type='bool', default='no')
    )

    required_if_args = [
      ["state", "present", ["username", "password"]],
      ["state", "absent", ["id"]]
    ]

    required_together_args = [
        ["password", "username"]
    ]

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
        required_if=required_if_args,
        required_together=required_together_args,
        supports_check_mode=False
    )

    ## General
    state = module.params['state']
    request_server = module.params['server_name']
    request_port = module.params['server_port']

    ## Authenticate
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

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

    try: 
        resp = json.loads(req.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    ## Payload
    if state == 'present':
        username = module.params['username']
        password = module.params['password']
        credtype = module.params['type']
        description = module.params['description']
        tag = module.params['tag']

        body = {
            'type': credtype, 
            'username': username, 
            'password': password, 
            'description': description
        }
        bodyjson = json.dumps(body)
        headers = {
            'x-api-version': '1.0-rev1',
            'Authorization': 'Bearer ' + resp['access_token'],
            'Content-Type': 'application/json'
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/credentials'

        method = "Post"
        req, info = fetch_url(module, request_url, headers=headers, method=method, data=bodyjson)

        if info['status'] != 200:
            module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

        try: 
            result['msg'] = json.loads(req.read())
            result['changed'] = True
        except AttributeError:
            module.fail_json(msg='Parsing Response Failed', **result)

    if state == 'absent':
        credid = module.params['id']

        headers = {
            'x-api-version': '1.0-rev1',
            'Authorization': 'Bearer ' + resp['access_token']
        }
        request_url = 'https://' + request_server + ':' + request_port + '/api/v1/credentials/' + credid

        method = "get"
        req, info = fetch_url(module, request_url, headers=headers, method=method)

        if info['status'] == 200:
            method = "Delete"
            req, info = fetch_url(module, request_url, headers=headers, method=method)

            if info['status'] != 200:
                module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

            try: 
                #result['msg'] = json.loads(req.read())
                result['changed'] = True
            except AttributeError:
                module.fail_json(msg='Parsing Response Failed', **result)

    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()