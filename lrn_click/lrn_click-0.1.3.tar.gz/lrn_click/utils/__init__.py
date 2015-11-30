def get_regions(ctx):
    "Get the AWS regions"
    import boto3

    ec2 = boto3.client('ec2')
    regions = [
        r.get('RegionName') for r in ec2.describe_regions().get('Regions', {})
    ]

    return sorted(regions)


def get_region_titles(ctx):
    import collections

    region_desc = {
        "ap-northeast-1": "Tokyo",
        "ap-southeast-1": "Singapore",
        "ap-southeast-2": "Sydney",
        "cn-north-1": "China",
        "eu-central-1": "Frankfurt",
        "eu-west-1": "Ireland",
        "sa-east-1": "Sao Paulo",
        "us-east-1": "Virginia",
        "us-west-1": "California",
        "us-west-2": "Oregon"
    }

    regions = {
        "{:<14} ({})".format(region_desc.get(r), r): r for r in get_regions(ctx)
    }

    return collections.OrderedDict(sorted(regions.items(), key=lambda t: t[1]))


def get_keypairs(ctx):
    "Get the key pairs"
    res = ctx.obj['ec2'].describe_key_pairs()
    return [k.get('KeyName') for k in res.get('KeyPairs', {})]
