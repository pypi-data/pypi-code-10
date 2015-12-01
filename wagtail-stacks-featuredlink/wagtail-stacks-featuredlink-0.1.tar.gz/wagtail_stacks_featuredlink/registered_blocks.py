from streamfield_tools.registry import block_registry

from .blocks import (
    stacks_featuredlink_button,
    stacks_featuredlinklist_block,
    stacks_featuredlink_anchor_tag
)

block_registry.register_block(
    'featured_link_list',
    stacks_featuredlinklist_block
)

block_registry.register_block(
    'button_link',
    stacks_featuredlink_button
)

block_registry.register_block(
    'anchor_tag',
    stacks_featuredlink_anchor_tag
)
