# Ansible Collection - veeamhub.veeam_rest

Documentation for the collection.

## Modules

### veeam_vbr_servercertificate_info

```
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
```
