#!/usr/bin/env python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: veeam_vbr_servercertificate_info

short_description: Get Current Veeam Backup Server Certificate from RestAPI.

version_added: "1.0.0"

description: Get Current Veeam Backup Server Certificate from RestAPI.

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
  - name: Test veeam_vbr_servercertificate_info
    veeamhub.veeam_rest.veeam_vbr_servercertificate_info:
        server_name: '10.0.2.16'
    register: testout
  - name: Debug Result
    debug:
        var: testout
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
"msg": {
    "automaticallyGenerated": false,
    "issuedBy": "Veeam Backup Server Certificate",
    "issuedTo": "Veeam Backup Server Certificate",
    "keyAlgorithm": "RSA-PKCS1-KeyEx",
    "keySize": "2048",
    "serialNumber": "1A17F5B55B2A169747FC7405CBEFFCE7",
    "subject": "CN=Veeam Backup Server Certificate",
    "thumbprint": "E2FFF23FD0A7A47A4D3C4689AD9371F874CC124E",
    "validBy": "2030-10-05T20:10:13+02:00",
    "validFrom": "2020-10-05T20:10:13+02:00"
'''

import json
import re
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        server_name=dict(type='str', required=True),
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

    request_server = module.params['server_name']
    request_port = module.params['server_port']
    headers = {
        'accept': 'application/json',
        'x-api-version': '1.0-rev1',
        'Authorization': 'true'
    }

    request_url = 'https://' + request_server + ':' + request_port + '/api/v1/serverCertificate'

    method = "Get"
    req, info = fetch_url(module, request_url, headers=headers, method=method)

    result['msg'] = json.loads(req.read())
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()