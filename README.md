### Setup MAAS
Assumes at least 13 systems with:
- 1TB spinning disk
- 10 cores
- 128 GiB RAM
- IPMI
- 1 x 1 gbit NIC, configured to PXE boot.
- 2 x 10 gbit NICs

All 1 gbit and 10 gbit NICs are assumed to be on the same flat network.

- Enlist and commission the nodes in MAAS
- Use setup-nodes.py to setup disk partitioning and bond interfaces.

Create a small (1 vcpu, 8gb ram, 50gb disk) VM on the MAAS server's host and enlist it.

### Deploy Openstack

Bootstrap to the vm on the maas host:

    juju bootstrap vpil-maas-controller vpil-maas --to=juju-controller-vm.maas --config test-mode=True

Deploy OpenStack

    juju deploy mutli-hypervisor.yaml

Wait for it to complete

For OIL, set up this symlink:

    ln -s common-config.oil common-config

For VPIL, set up this symlink:

    ln -s common-config.vpil-network common-config

Setup OpenStack

    ./setup-openstack

Bootstrap juju on OpenStack
---------------------------
To bootstrap juju 2:

    ./bootstrap-juju2
