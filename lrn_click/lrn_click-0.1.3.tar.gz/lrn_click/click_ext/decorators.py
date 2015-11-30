import click


def region(*param_decls, **attrs):
    def decorator(f):
        from lrn_click.click_ext.core import OptionPicker
        from lrn_click.click_ext.types import AWSRegionParamType
        from lrn_click.utils import get_region_titles

        attrs.setdefault("type", AWSRegionParamType())
        attrs.setdefault("is_eager", True)
        attrs.setdefault("prompt_list_func", get_region_titles)
        attrs.setdefault("prompt_title", click.style(
            "Select the AWS region", fg="magenta"))
        attrs.setdefault("prompt", click.style(
            "Enter choice", fg="yellow"))

        click.decorators._param_memo(f, OptionPicker(param_decls, **attrs))
        return f

    return decorator


def prefix(*param_decls, **attrs):
    def decorator(f):
        from lrn_click.click_ext.types import VpcPrefixParamType

        attrs.setdefault("type", VpcPrefixParamType())
        attrs.setdefault("prompt", click.style(
            "Enter a VPC prefix (eg. prod, stg, test)", fg="yellow"))

        click.decorators._param_memo(f, click.Option(param_decls, **attrs))
        return f

    return decorator


def num_of_azs(*param_decls, **attrs):
    def decorator(f):
        from lrn_click.click_ext.types import VpcNumOfAZsParamType

        attrs.setdefault("type", VpcNumOfAZsParamType())
        attrs.setdefault("prompt", click.style(
            "Enter number of AZs to cover", fg="yellow"))

        click.decorators._param_memo(f, click.Option(param_decls, **attrs))
        return f

    return decorator


def cidr(*param_decls, **attrs):
    def decorator(f):
        from lrn_click.click_ext.types import VpcCIDRParamType

        class CIDROption(click.Option):
            def __init__(self, param_decls=None, layer_mask=None,
                         num_of_layers=None, **attrs):
                click.Option.__init__(self, param_decls, **attrs)
                self.layer_mask = layer_mask
                self.num_of_layers = num_of_layers

        attrs.setdefault("type", VpcCIDRParamType())
        attrs.setdefault("prompt", click.style("Enter VPC CIDR", fg="yellow"))
        attrs.setdefault("layer_mask", 24)
        attrs.setdefault("num_of_layers", 3)

        click.decorators._param_memo(f, CIDROption(param_decls, **attrs))
        return f

    return decorator


def keypair(*param_decls, **attrs):
    def decorator(f):
        from lrn_click.click_ext.core import OptionPicker
        from lrn_click.click_ext.types import VpcKeyPairParamType
        from lrn_click.utils import get_keypairs

        attrs.setdefault("type", VpcKeyPairParamType())
        attrs.setdefault("prompt_list_func", get_keypairs)
        attrs.setdefault("prompt_title", click.style(
            "Select the key pair", fg="magenta"))
        attrs.setdefault("prompt", click.style(
            "Enter choice", fg="yellow"))
        attrs.setdefault("prompt_pick_single", True)

        click.decorators._param_memo(f, OptionPicker(param_decls, **attrs))
        return f

    return decorator
