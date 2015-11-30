__author__ = 'gabriel'
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import argparse
import atexit
import getpass
from os.path import expanduser
import ConfigParser
from tools import clone_vm, get_obj, unregister_vm, get_vm_by_name, delete_file_from_datastore, delete_folder_from_datastore
from vclones.smtp import send_email_notifications
from sys import stdout

# Fix for self signed certificates

import requests
requests.packages.urllib3.disable_warnings()

import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


config = ConfigParser.ConfigParser()
config.read(['esxi.ini', expanduser('/etc/esxi.ini')])

VMS = []


def GetObject(content, vimtype, name):
    """
    Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def GetArgs():
    """
    Supports the command-line arguments listed below.
    """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')
    parser.add_argument(
        '-s', '--host', required=True, action='store', help='Remote host to connect to'
    )
    parser.add_argument(
        '-o', '--port', type=int, default=443, action='store', help='Port to connect on'
    )
    parser.add_argument(
        '-u', '--user', required=True, action='store', help='User name to use when connecting to host'
    )
    parser.add_argument(
        '-p', '--password', required=False, action='store', help='Password to use when connecting to host'
    )
    parser.add_argument(
        '-v', '--vm', required=False, action='store', help='Select the VM to clone'
    )
    args = parser.parse_args()
    return args


def clone_all_vms(vm, depth=1):
    """
    Print information for a particular virtual machine or recurse into a folder
     with depth protection
    """
    maxdepth = 10

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        if depth > maxdepth:
            return
        vm_list = vm.childEntity
        for c in vm_list:
            clone_all_vms(c, depth+1)
        return

    summary = vm.summary
    print("Name       : ", summary.config.name)
    print("Path       : ", summary.config.vmPathName)
    print("Guest      : ", summary.config.guestFullName)
    annotation = summary.config.annotation
    if annotation is not None and annotation != "":
        print("Annotation : ", annotation)
    print("State      : ", summary.runtime.powerState)
    if summary.guest is not None:
        ip = summary.guest.ipAddress
        if ip is not None and ip != "":
            print("IP         : ", ip)
    if summary.runtime.question is not None:
        print("Question  : ", summary.runtime.question.text)
    stdout.flush()
    if summary.runtime.powerState == 'poweredOn':
        vm_name = summary.config.name
        ctask = clone_vm(
            si.RetrieveContent(),
            get_obj(si.RetrieveContent(), [vim.VirtualMachine], summary.config.name),
            '{0}-clone'.format(summary.config.name),
            si,
            config.get('storage', 'datacenter'),
            None,
            config.get('storage', 'clone-storage'),
            config.get('storage', 'cluster'),
            None,
            False
        )
        print(ctask)
        if ctask.info.state == 'error':
            print(ctask.info.error.msg)
            VMS.append({
                'name': vm_name,
                'status': ctask.info.error.msg
            })
        else:
            print('Get cloned vm')
            cloned_vm = get_vm_by_name(si, '{0}-clone'.format(summary.config.name))
            print('Get cloned vm dir')
            cloned_vm_dir = get_vm_by_name(si, '{0}-clone'.format(summary.config.name)).config.files.logDirectory
            print('Unregistering vm')
            unregister_vm(
                vm=cloned_vm
            )
            print(cloned_vm_dir)
            if cloned_vm_dir == '[{0}] {1}-clone/'.format(config.get('storage', 'clone-storage'), summary.config.name):
                try:
                    delete_folder_from_datastore(
                        si.RetrieveContent(),
                        config.get('storage', 'clone-storage'),
                        config.get('storage', 'datacenter'),
                        '[{1}] {0}-clone_1'.format(summary.config.name, config.get('storage', 'clone-storage'))
                    )
                    VMS.append({
                        'name': summary.config.name,
                        'status': 'Done'
                    })
                except vim.fault.CannotDeleteFile as e:
                    VMS.append({
                        'name': summary.config.name,
                        'status': e.msg
                    })
            else:
                try:
                    delete_folder_from_datastore(
                        si.RetrieveContent(),
                        config.get('storage', 'clone-storage'),
                        config.get('storage', 'datacenter'),
                        '[{1}] {0}-clone'.format(summary.config.name, config.get('storage', 'clone-storage'))
                    )
                    VMS.append({
                        'name': summary.config.name,
                        'status': 'Done'
                    })
                except vim.fault.CannotDeleteFile as e:
                    VMS.append({
                        'name': summary.config.name,
                        'status': e.msg
                    })

    print("")


def connect(host, user, pwd, port):
    """
    Create connection to vmware host
    """
    global si

    si = SmartConnect(
        host=host,
        user=user,
        pwd=pwd,
        port=int(port)
    )

    return si


def batch():
    """
    Start cloning vms referring configuration writed on esxi.ini only
    """
    connect(
        host=config.get('vmware', 'host'),
        user=config.get('vmware', 'user'),
        pwd=config.get('vmware', 'pwd'),
        port=config.getint('vmware', 'port')
    )

    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for vm in vm_list:
                clone_all_vms(vm)
            return 0

    if config.getboolean('notification', 'enabled'):
        send_email_notifications(
            vms=VMS,
            host=config.get('vmware', 'host'),
            datacenter=config.get('storage', 'datacenter'),
            cluster=config.get('storage', 'cluster'),
            rcpt_from=config.get('notification', 'from'),
            rcpt_to=config.get('notification', 'to'),
            smtp_host=config.get('notification', 'host')
        )

def test():
    """
    Simpel command-line program for testing clones work
    """
    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.host, args.user))
    connect(
        host=args.host,
        user=args.user,
        pwd=password,
        port=int(args.port)
    )
    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for vm in vm_list:
                try:
                    if vm.summary.config.name == args.vm:
                        clone_all_vms(vm)
                except:
                    pass
            return 0

def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """
    args = GetArgs()
    if args.password:
        password = args.password
    else:
        password = getpass.getpass(prompt='Enter password for host %s and user %s: ' % (args.host, args.user))

    connect(
        host=args.host,
        user=args.user,
        pwd=password,
        port=int(args.port)
    )
    if not si:
        print("Could not connect to the specified host using specified "
              "username and password")
        return -1

    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vm_folder = datacenter.vmFolder
            vm_list = vm_folder.childEntity
            for vm in vm_list:
                clone_all_vms(vm)
            return 0

# Start program
if __name__ == "__main__":
   main()