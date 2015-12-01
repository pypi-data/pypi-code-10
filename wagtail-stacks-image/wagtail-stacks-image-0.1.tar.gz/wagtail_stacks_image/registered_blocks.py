from streamfield_tools.registry import block_registry

from .blocks import (
    stacks_image_block,
    stacks_imagelist_block
)

block_registry.register_block(
    'image',
    stacks_image_block
)

block_registry.register_block(
    'image_list',
    stacks_imagelist_block
)
