import sys
import argparse
from .gcloud import GCloud
from .digitalocean import DigitalOcean
from .aws import AWS
from .constants import COLUMNS_MAPPER


def add_flags(parser):
    parser.add_argument('-f', '--fields', type=str, help='Specified fields to retrieve(comma - seperated)', required=False)
    parser.add_argument('-d', '--delimiter', type=str, help='Delimiter (default is " | " with spaces)', required=False)
    parser.add_argument('-o', '--omit-columns', help='Omit Columns', action="store_true")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    subparser = parser.add_subparsers(dest='askme')

    # gcloud parser
    gcloud_parser = subparser.add_parser('gcloud')
    gcloud_subparser = gcloud_parser.add_subparsers(dest='gcloud')
    gce_zone_parser = gcloud_subparser.add_parser('gce-zone')
    gce_machine_type_parser = gcloud_subparser.add_parser('gce-machine-type')
    gce_disk_type_parser = gcloud_subparser.add_parser('gce-disk-type')
    gce_image_parser = gcloud_subparser.add_parser('gce-image')
    add_flags(gce_zone_parser)
    add_flags(gce_machine_type_parser)
    add_flags(gce_disk_type_parser)
    add_flags(gce_image_parser)

    # digitalocean parser
    do_parser = subparser.add_parser('do')
    do_subparser = do_parser.add_subparsers(dest='do')
    do_region_parser = do_subparser.add_parser('region')
    do_size_parser = do_subparser.add_parser('size')
    do_dist_image_parser = do_subparser.add_parser('dist-image')
    do_app_image_parser = do_subparser.add_parser('app-image')
    add_flags(do_region_parser)
    add_flags(do_size_parser)
    add_flags(do_dist_image_parser)
    add_flags(do_app_image_parser)

    # aws parser
    aws_parser = subparser.add_parser('aws')
    aws_subparser = aws_parser.add_subparsers(dest='aws')
    ec2_region_parser = aws_subparser.add_parser('ec2-region')
    ec2_zone_parser = aws_subparser.add_parser('ec2-zone')
    ec2_instance_type_parser = aws_subparser.add_parser('ec2-instance-type')
    add_flags(ec2_region_parser)
    add_flags(ec2_zone_parser)
    add_flags(ec2_instance_type_parser)

    args = parser.parse_args(sys.argv[1:])

    fields = args.fields.split(",") if args.fields else COLUMNS_MAPPER.keys()
    delimiter = args.delimiter if args.delimiter else " | "

    options = {
        "fields": fields,
        "delimiter": delimiter,
        "omit_columns": args.omit_columns,
    }

    subcommand = getattr(args, args.askme)
    if hasattr(args, 'gcloud'):
        gcloud = GCloud(options)
        if subcommand == "gce-zone":
            gcloud.render_gce_zone()
        elif subcommand == "gce-machine-type":
            gcloud.render_gce_machine_type()
        elif subcommand == "gce-disk-type":
            gcloud.render_gce_disk_type()
        elif subcommand == "gce-image":
            gcloud.render_gce_image()
        else:
            raise Exception("No matching sub-command for gcloud")

    elif hasattr(args, 'do'):
        do = DigitalOcean(options)
        if subcommand == "region":
            do.render_region()
        elif subcommand == "size":
            do.render_size()
        elif subcommand == "dist-image":
            do.render_dist_image()
        elif subcommand == "app-image":
            do.render_app_image()
        else:
            raise Exception("No matching sub-command for digitalocean")

    elif hasattr(args, 'aws'):
        aws = AWS(options)
        if subcommand == "ec2-region":
            aws.render_ec2_region()
        elif subcommand == "ec2-zone":
            aws.render_ec2_zone()
        elif subcommand == "ec2-instance-type":
            aws.render_ec2_instance_type()
        else:
            raise Exception("No matching sub-command for aws")

    else:
        raise Exception("No matching sub-command for askme")
