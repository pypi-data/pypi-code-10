import boto
import boto.ec2
import boto.vpc
import boto.utils
import functools

# global cache of queried data
__cache = {}


def cached(f):
    @functools.wraps(f)
    def with_caching(*args, **kwargs):
        name = f.__name__
        if name in __cache:
            return __cache[name]
        result = f(*args, **kwargs)
        __cache[name] = result
        return result
    return with_caching


def cache():
    return __cache


@cached
def instance_metadata():
    return boto.utils.get_instance_metadata()


@cached
def region():
    return availability_zone()[:-1]


@cached
def availability_zone():
    im = instance_metadata()
    return im['placement']['availability-zone']


@cached
def vpc_id():
    im = instance_metadata()
    macs = im['network']['interfaces']['macs']
    assert len(macs.keys()) == 1
    mac = macs.keys()[0]
    return macs[mac]['vpc-id']


@cached
def vpc_name():
    vpc_conn = boto.vpc.connect_to_region(region())
    vpcs = vpc_conn.get_all_vpcs(vpc_ids=[vpc_id()])
    assert len(vpcs) == 1, \
        'Should have one vpc with id={}, not {}'.format(vpc_id(), vpcs)
    return vpcs[0].tags.get('Name')


@cached
def instance_id():
    return instance_metadata()['instance-id']


@cached
def instance_tags():
    ec2 = boto.ec2.connect_to_region(region())
    instances = ec2.get_only_instances(instance_ids=[instance_id()])
    assert len(instances) == 1, \
        'Should have one instance with id={}, not {}'.format(
            instance_id(), instances)
    return instances[0].tags


@cached
def instance_name():
    return instance_tags().get('Name')
