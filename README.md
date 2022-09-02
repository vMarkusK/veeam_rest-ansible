# Ansible Collection - veeamhub.veeam_rest

<p align="left">
  <a href="https://github.com/vMarkusK/veeam_rest-ansible/actions?query=workflow%3ABasicLint"><img alt="Ansible-Test BasicLint" src="https://github.com/vMarkusK/veeam_rest-ansible/workflows/BasicLint/badge.svg"></a>
</p>


Documentation for the veeam_rest Ansible Collection.

## Modules

### veeam_vbr_servercertificate_info

Get Current Veeam Backup Server Certificate from RestAPI.

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
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

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
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

**Please note** This is an MVP with very limited functionality

Known Limitations:
- Not idempotent

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Test veeam_vbr_credentials Create
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
        type: 'Linux'
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
        server_password: '<Password>'
        id: "{{ create_cred.msg.id }}"
        state: absent
    register: delete_cred
  - name: Debug Result
    debug:
        var: delete_cred
```

### veeam_vbr_repositories_info

Get Veeam Backup & Replication Repositories.

**Please note** This is an MVP with very limited functionality

Known Limitations:
- No SOBR listing

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
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

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
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

### veeam_vbr_jobs_info

Get Veeam Backup & Replication Jobs.


```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Get VBR Jobs
    veeamhub.veeam_rest.veeam_vbr_jobs_info:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
    register: job_testout
  - name: Debug VBR Jobs Result
    debug:
        var: job_testout
```

### veeam_vbr_jobs_manage

Add and Delete Veeam Backup & Replication Jobs.


**Please note** This is an MVP with very limited functionality

Known Limitations:
- Only vSphere Jobs with a single VM
- Not idempotent
- No Options

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
  tasks:
  - name: Create VBR Jobs
    veeamhub.veeam_rest.veeam_vbr_jobs_mange:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
        state: present
        jobName: 'Ansible Test'
        hostName: 'vcenter01'
        name: 'test01'
        objectId: 'vm-0815'
        type: 'VirtualMachine'
        description: 'My Test'
        backupRepositoryId: 'e61b4d0e-a9ef-4cae-be94-c45a7f3915b2'
    register: job_testout
  - name: Debug VBR Jobs Result
    debug:
        var: job_testout
  - name: Delete VBR Jobs
    veeamhub.veeam_rest.veeam_vbr_jobs_mange:
        server_name: '10.0.2.16'
        server_username: 'Administrator'
        server_password: '<Password>'
        state: absent
        id: 'e61b4d0e-a9ef-4cae-be94-c45a7f3915b2'
```