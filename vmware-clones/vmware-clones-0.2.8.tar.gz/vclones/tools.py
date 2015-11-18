__author__ = 'gabriel'

from pyVmomi import vim


def get_vm_by_name(si, vmname):
    content = si.content
    obj_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
    vm_list = obj_view.view
    obj_view.Destroy()

    for vm in vm_list:
        if vm.name == vmname:
            return vm

    return None


def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print "there was an error"
            #task_error = task.info.error.msg
            task_done = True


def unregister_vm(vm):
    return vm.UnregisterVM()


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj

def delete_folder_from_datastore(content, datacenter_name, folder):
    """
    Delete file or folder(not empty too) from datastore.
    """
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
    task = vim.FileManager.DeleteDatastoreFile_Task(
        content.fileManager,
        folder,
        datacenter
    )
    wait_for_task(task)

def delete_file_from_datastore(content, datastore_name, path):
    """
    Delete a single file or empty folder on given datastore
    """
    try:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
        datastore.browser.DeleteFile('[{0}] {1}'.format(datastore_name, path))
    except vim.fault.FileNotFound as e:
        return e
    return None


def move_file_on_datastore(content, datastore_name, datacenter_name, source, destination):
    """
    Move file or folder (Fail if destination already exists)
    """
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)
    datastore = get_obj(content, [vim.Datastore], datastore_name)
    task = vim.FileManager.MoveDatastoreFile_Task(
        content.fileManager,
        '[{0}] {1}'.format(datastore_name, source),
        datacenter,
        '[{0}] {1}'.format(datastore_name, destination),
        datacenter,
        True
    )
    wait_for_task(task)



def search_file_on_datastore(content, datastore_name, path):
    """
    Fix needed
    """
    datastore = get_obj(content, [vim.Datastore], datastore_name)
    return datastore.browser


def clone_vm(
        content, template, vm_name, si,
        datacenter_name, vm_folder, datastore_name,
        cluster_name, resource_pool, power_on):
    """
    Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
    cluster_name, resource_pool, and power_on are all optional.
    """

    # if none git the first one
    datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

    if vm_folder:
        destfolder = get_obj(content, [vim.Folder], vm_folder)
    else:
        destfolder = datacenter.vmFolder

    if datastore_name:
        datastore = get_obj(content, [vim.Datastore], datastore_name)
    else:
        datastore = get_obj(
            content, [vim.Datastore], template.datastore[0].info.name)

    # if None, get the first one
    cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool

    # set relospec
    relospec = vim.vm.RelocateSpec()
    relospec.datastore = datastore
    relospec.pool = resource_pool

    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    clonespec.powerOn = power_on

    print "cloning VM..."
    task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
    wait_for_task(task)
    return task