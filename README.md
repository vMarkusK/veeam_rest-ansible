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
        server_name: '<VBR Host>'
    register: testout
  - name: Debug Result
    ansible.builtin.debug:
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
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: testout
  - name: Debug Result
    ansible.builtin.debug:
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
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
        type: 'Linux'
        username: 'root'
        password: '<Password>'
        description: 'Created by Ansible RestAPI Module'
    register: create_cred
  - name: Debug Result
    ansible.builtin.debug:
        var: create_cred
  - name: Test veeam_vbr_credentials Delete
    veeamhub.veeam_rest.veeam_vbr_credentials:
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
        id: "{{ create_cred.msg.id }}"
        state: absent
    register: delete_cred
  - name: Debug Result
    ansible.builtin.debug:
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
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: testout
  - name: Debug Result
    ansible.builtin.debug:
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
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: testout
  - name: Debug Result
    ansible.builtin.debug:
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
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: job_testout
  - name: Debug VBR Jobs Result
    ansible.builtin.debug:
        var: job_testout
```

### veeam_vbr_jobs_manage

Add and Delete Veeam Backup & Replication Jobs.

**Please note** This is an MVP with very limited functionality

Known Limitations:
- Only vSphere Jobs with a single VM
- Not idempotent
- No Options

End-to-End Create Veeam Job and vSphere VM:

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
  vars:
    repos_query: "infrastructure_repositories.data[?name=='Local01']"
    vcenter_hostname: "<vCenter Host>"
    vcenter_username: "<vCenter User>"
    vcenter_password: "<vCenter Password>"
    vm_datacenter: "<vCenter DC>"
    vm_cluster: "<vCenter Cluster>"
    vm_name: "Ansible_Test"
    vm_folder: "<vCenter Folder>"
    vm_datastore: "<Datastore Name>"
    vm_network: "<Network Name>"
  tasks:
  - name: Create vSphere VM {{ vm_name }}
    community.vmware.vmware_guest:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: yes
        datacenter: "{{ vm_datacenter }}"
        cluster: "{{ vm_cluster }}"
        folder: "{{ vm_folder }}"
        name: "{{ vm_name }}" 
        state: poweredoff
        guest_id: "rhel8_64Guest"
        datastore: "{{ vm_datastore }}"
        disk:
          - size_gb: "16"
        hardware:
            version: 19
            memory_mb: 2048
            memory_reservation_lock: false
            num_cpus: 1
            scsi: paravirtual
            boot_firmware: efi
        networks:
          - name: "{{ vm_network }}"
            device_type: vmxnet3
        advanced_settings:
          - key: "ctkEnabled"
            value: "True"
        wait_for_ip_address: no
    register: deploy_vm
  - name: VBR API-Test
    veeamhub.veeam_rest.veeam_vbr_servercertificate_info:
        server_name: '<VBR Host>'
    register: api_testout
  - name: Debug VBR API-Test Result
    ansible.builtin.debug:
        var: api_testout
  - name: Get VBR Repos
    veeamhub.veeam_rest.veeam_vbr_repositories_info:
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: repo_testout
  - name: Debug VBR Repos Result
    ansible.builtin.debug:
        var: repo_testout | json_query(repos_query)
  - name: Filter Repo Object
    set_fact: 
      repo_id: "{{ repo_testout | json_query(repos_id_query) }}"
    vars:
      repos_id_query: 'infrastructure_repositories.data[?name==`Local01`].id'
  - name: Create VBR Job
    veeamhub.veeam_rest.veeam_vbr_jobs_manage:
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
        state: present
        jobName: 'Ansible Test'
        hostName: "{{ vcenter_hostname }}"
        name: "{{ vm_name }}"
        objectId: "{{ deploy_vm.instance.moid }}"
        type: 'VirtualMachine'
        description: 'My Test'
        backupRepositoryId: "{{ repo_id[0] }}"
    register: job_createout
  - name: Debug VBR Jobs Result
    ansible.builtin.debug:
        var: job_createout   

```

Endt-to-End Delete Veeam Job and vSphere VM:

```yaml
- name: Test Veeam RestAPI Collection
  hosts: localhost
  gather_facts: false
  vars:
    jobs_query: "infrastructure_jobs.data[?name=='Ansible Test']"
    vcenter_hostname: "<vCenter Host>"
    vcenter_username: "<vCenter User>"
    vcenter_password: "<vCenter Password>"
    vm_datacenter: "<vCenter DC>"
    vm_cluster: "<vCenter Cluster>"
    vm_name: "Ansible_Test"
    vm_folder: "<vCenter Folder>"
  tasks:
  - name: Delete vSphere VM {{ vm_name }}
    community.vmware.vmware_guest:
        hostname: "{{ vcenter_hostname }}"
        username: "{{ vcenter_username }}"
        password: "{{ vcenter_password }}"
        validate_certs: yes
        datacenter: "{{ vm_datacenter }}"
        cluster: "{{ vm_cluster }}"
        folder: "{{ vm_folder }}"
        name: "{{ vm_name }}" 
        state: absent
    register: Delete_vm
  - name: Get VBR Jobs
    veeamhub.veeam_rest.veeam_vbr_jobs_info:
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
    register: job_testout
  - name: Debug VBR Jobs Result
    ansible.builtin.debug:
        var: job_testout | json_query(jobs_query)
  - name: Filter Job Object
    set_fact: 
      job_id: "{{ job_testout | json_query(jobs_id_query) }}"
    vars:
      jobs_id_query: 'infrastructure_jobs.data[?name==`Ansible Test`].id'
  - name: Delete VBR Job
    veeamhub.veeam_rest.veeam_vbr_jobs_manage:
        server_name: '<VBR Host>'
        server_username: '<VBR User>'
        server_password: '<VBR Password>'
        state: absent
        id: "{{ job_id[0] }}"
```