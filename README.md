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
### veeam_vbr_credentials_info

```
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
```

### veeam_vbr_credentials

```
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
  - name: Test veeam_vbr_credentials Create
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: 'Anfang!!'
        type: 'Linux'
        username: 'root'
        password: 'C0mPl3x!'
        description: 'Created by Ansible RestAPI Module'
    register: create_cred
  - name: Debug Result
    debug:
        var: create_cred
  - name: Test veeam_vbr_credentials Delete
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: 'Anfang!!'
        id: "{{ create_cred.msg.id }}"
        state: absent
    register: delete_cred
  - name: Debug Result
    debug:
        var: delete_cred
```

### veeam_vbr_repositories_info

```
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
  - name: Test veeam_vbr_repositories_info
    veeamhub.veeam_rest.veeam_vbr_repositories_info:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
    register: testout
  - name: Debug Result
    debug:
        var: testout
```

### veeam_vbr_managedservers_info

```
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
```