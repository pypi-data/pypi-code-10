# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.ec2 import (output_ec2_list, output_ec2_info,
                             output_ami_list, output_ami_info,
                             output_ec2_summary)
from acli.connections import get_client


def ec2_summary(aws_config=None):
    """
    @type aws_config: Config
    """
    elb_client = get_client(client_type='elb', config=aws_config)
    ec2_client = get_client(client_type='ec2', config=aws_config)
    elbs = len(elb_client.describe_load_balancers().get('LoadBalancerDescriptions'))
    instances = len(list(ec2_client.describe_instances().get('Reservations', [])))
    amis = len(list(ec2_client.describe_images(Owners=['self']).get('Images')))
    secgroups = len(ec2_client.describe_security_groups().get('SecurityGroups', 0))
    addresses = ec2_client.describe_addresses()['Addresses']
    eips = len([x for x, _ in enumerate(addresses)])
    summary = {'instances': instances, 'elbs': elbs, 'eips': eips,
               'amis': amis, 'secgroups': secgroups}
    output_ec2_summary(output_media='console', summary=summary)
    exit(0)


def ec2_list(aws_config=None):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    instances_req = ec2_client.describe_instances()
    reservations = instances_req.get('Reservations')
    all_instances = list()
    for reservation in reservations:
        for instance in reservation.get('Instances'):
            all_instances.append(instance)

    if len(list(all_instances)):
        output_ec2_list(output_media='console', instances=all_instances)
    exit('No ec2 instances found.')


def ec2_info(aws_config=None, instance_id=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    ec2_query = ec2_client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [instance_id]}])
    reservations = ec2_query.get('Reservations')
    try:
        instance = reservations[0].get('Instances')[0]
        if instance.get('InstanceId', None):
            output_ec2_info(output_media='console',
                            instance=instance)
    except IndexError:
        raise SystemExit("Cannot find instance: {0}".format(instance_id))


def ec2_manage(aws_config=None, instance_id=None, action=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    @type action: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance = reservations.get('Reservations')[0].get('Instances')[0]
    try:
        instance_id = instance.get('InstanceId')
        instance_state = instance['State']['Name']
        if instance_id:
            if action == 'stop':
                if instance_state in ('pending', 'rebooting', 'stopping', 'terminated', 'shutting-down'):
                    exit("Cannot stop instance as state is {0}.".format(instance_state))
                elif instance_state in ('stopping', 'stopped', 'shutting-down'):
                    exit("Instance {0} is already {1}.".format(instance_id, instance_state))
                else:
                    instance.stop()
                    exit("Instance {0} stopping.".format(instance_id))
            if action == 'start':
                if instance_state in ('rebooting', 'stopping',
                                      'terminated', 'shutting-down'):
                    exit("Cannot start instance {0} as state is {1}.".format(instance_id,
                                                                             instance_state))
                elif instance_state in ('pending', 'rebooting',
                                        'stopping', 'terminated',
                                        'shutting-down', 'running'):
                    exit("Instance {0} is already {1}.".format(instance_id, instance_state))
                else:
                    instance.start()
                    exit("Instance {0} starting.".format(instance_id))
            if action == 'reboot':
                if instance_state in ('pending', 'stopping', 'terminated', 'shutting-down'):
                    exit("Cannot reboot instance {0} as state is {1}.".format(instance_id,
                                                                              instance_state))
                elif instance_state == 'rebooting':
                    exit("Instance {0} is already {1}.".format(instance_id, instance_state))
                else:
                    instance.reboot()
                    exit("Instance {0} rebooting.".format(instance_id))
            if action == 'terminate':
                if instance_state in ('rebooting', 'stopping',
                                      'terminated', 'shutting-down'):
                    exit("Cannot terminate instance {0} as state is {1}.".format(instance_id,
                                                                                 instance_state))
                elif instance_state in ('rebooting',
                                        'stopping', 'terminated',
                                        'shutting-down'):
                    exit("Instance {0} is already {1}.".format(instance_id, instance_state))
                else:
                    instance.terminate()
                    exit("Instance {0} terminating.".format(instance_id))
    except AttributeError:
        exit("Cannot find instance: {0}".format(instance_id))


def ami_info(aws_config=None, ami_id=None):
    """
    @type aws_config: Config
    @type ami_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    output_ami_info(output_media='console',
                    ami=ec2_client.describe_images(ImageIds=[ami_id]).get('Images')[0])


def ami_list(aws_config):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    output_ami_list(output_media='console',
                    amis=ec2_client.describe_images(Owners=['self']).get('Images'))


def ec2_get_instance_vols(aws_config=None, instance_id=None):
    """
    @type aws_config: Config
    @type instance_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    reservations = ec2_client.describe_instances(InstanceIds=[instance_id])
    reservation = reservations.get('Reservations')[0]
    instance = reservation.get('Instances')[0]
    vols = list()
    for bdm in instance.get('BlockDeviceMappings'):
        vols.append(bdm)
    return vols
