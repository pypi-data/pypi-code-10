# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
from acli.output.vpc import (output_vpc_list, output_vpc_info)
from acli.connections import get_client
from botocore.exceptions import ClientError


def vpc_list(aws_config=None):
    """
    @type aws_config: Config
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    vpcs = ec2_client.describe_vpcs()
    if vpcs.get('Vpcs', None):
        output_vpc_list(output_media='console', vpcs=vpcs)
    else:
        exit("No VPCs found.")


def vpc_info(aws_config=None, vpc_id=None):
    """
    @type aws_config: Config
    @type vpc_id: unicode
    """
    ec2_client = get_client(client_type='ec2', config=aws_config)
    try:
        vpcs = ec2_client.describe_vpcs(VpcIds=[vpc_id])
        all_subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        output_vpc_info(output_media='console', vpc=vpcs['Vpcs'][0], subnets=all_subnets)
    except (ClientError, IndexError):
        exit("Cannot find VPC: {0}".format(vpc_id))
