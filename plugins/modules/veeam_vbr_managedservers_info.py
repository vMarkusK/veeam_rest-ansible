#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: veeam_vbr_managedservers_info

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
  - name: Test veeam_vbr_managedservers_info
    veeamhub.veeam_rest.veeam_vbr_managedservers_info:
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
{
    "credentialsId": "00000000-0000-0000-0000-000000000000",
    "description": "Backup server",
    "id": "6745a759-2205-4cd2-b172-8ec8f7e60ef8",
    "name": "WIN-RT26QHK0M11",
    "networkSettings": {
        "components": [
            {
                "componentName": "DeployerSvc",
                "port": 6160
            },
            {
                "componentName": "Transport",
                "port": 6162
            },
            {
                "componentName": "Nfs",
                "port": 6161
            },
            {
                "componentName": "RestoreProxy",
                "port": 6170
            },
            {
                "componentName": "WanAccelerator",
                "port": 6164
            },
            {
                "componentName": "Tape",
                "port": 6166
            },
            {
                "componentName": "CloudGate",
                "port": 6168
            },
            {
                "componentName": "AgentConfigureService",
                "port": 9380
            },
            {
                "componentName": "FileSystemVssIntegration",
                "port": 6210
            },
            {
                "componentName": "VssHwSnapshotProvider",
                "port": 6211
            }
        ],
        "portRangeEnd": 3300,
        "portRangeStart": 2500,
        "serverThisSide": false
    },
    "type": "WindowsHost"
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

    # Authenticate
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

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

    try:
        resp = json.loads(req.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    # Payload
    headers = {
        'x-api-version': '1.0-rev1',
        'Authorization': 'Bearer ' + resp['access_token']
    }
    request_url = 'https://' + request_server + ':' + request_port + '/api/v1/backupInfrastructure/managedServers'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    if info['status'] != 200:
        module.fail_json(msg="Fail: %s" % ("Status: " + str(info['status']) + ", Message: " + str(info['msg'])))

    try:
        result['infrastructure_managedservers'] = json.loads(req.read())
    except AttributeError:
        module.fail_json(msg='Parsing Response Failed', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
