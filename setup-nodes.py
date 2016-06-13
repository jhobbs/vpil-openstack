#!/usr/bin/env python3

import json
from subprocess import check_output


def cmd(cmd_string, parse=True):
    maas_cmd = "maas root " + cmd_string
    print(maas_cmd)
    output = check_output(maas_cmd.split(" ")).decode("utf-8")
    if parse:
       return json.loads(output)
    else:
       return output


def get_nodes():
    node_list = cmd("nodes read")
    for node in node_list:
        if 'service_set' in node:
            continue
        yield node


def clear_partitions(system_id, blockdevice):
    print("clearing partitions from %s" % (blockdevice['id_path']))
    for partition in blockdevice['partitions']:
        cmd("partition delete %s %s %s" % (
            system_id, blockdevice['id'], partition['id']), parse=False)
    if blockdevice['filesystem'] is not None:
        cmd("block-device unmount %s %s" % (system_id, blockdevice['id']))
        cmd("block-device unformat %s %s" % (system_id, blockdevice['id']))


def create_partition(system_id, blockdevice_id, size, fstype,
                     label, mount_point):
    results = cmd("partitions create %s %s size=%s" % (
        system_id, blockdevice_id, size))
    partition_id = results['id']
    cmd("partition format %s %s %s fstype=%s label=%s" % (
        system_id, blockdevice_id, partition_id, fstype, label))
    cmd("partition mount %s %s %s mount_point=%s" % (
        system_id, blockdevice_id, partition_id, mount_point))


def setup_root_blockdevice(system_id, blockdevice_id):
    cmd(
        "block-device set-boot-disk %s %s" % (system_id, blockdevice_id),
        parse=False)
    # just using the size that maas used automatically on the nvme device.
    create_partition(
        system_id, blockdevice_id, size=536870912,
        fstype='fat32', label='efi', mount_point='/boot/efi')
    # just hard coding the known left over side, could read from maas.
    create_partition(
        system_id, blockdevice_id, size=999662026752,
        fstype='ext4', label='root', mount_point='/')


def main():
    for node in get_nodes():
        for blockdevice in node['blockdevice_set']:
            clear_partitions(node['system_id'], blockdevice)
            if blockdevice['path'] == '/dev/disk/by-dname/sda':
                setup_root_blockdevice(node['system_id'], blockdevice['id'])


if __name__ == '__main__':
    main()