# Ansible Collection - veeamhub.veeam_rest

<p align="left">
  <a href="https://github.com/vMarkusK/veeam_rest-ansible/actions?query=workflow%3ABasicLint"><img alt="Ansible-Test BasicLint" src="https://github.com/vMarkusK/veeam_rest-ansible/workflows/BasicLint/badge.svg"></a>
</p>


Documentation for the veeam_rest Ansible Collection.

## Modules

### veeam_vbr_servercertificate_info

Get Current Veeam Backup Server Certificate from RestAPI.

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

Get Veeam Backup & Replication Credentials.

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

Add and Remove Veeam Backup & Replication Credentials.

```
- name: Test Veeam RestAPI Collection
  hosts: localhost
  tasks:
  - name: Test veeam_vbr_credentials Create
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: 'Anfang!!'
        type: 'linux'
        username: 'root'
        password: '<Password>'
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

Get Veeam Backup & Replication Repositories.

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

Get Veeam Backup & Replication Managed Servers.

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