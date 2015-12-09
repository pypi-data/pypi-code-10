from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock

from streamfield_tools.registry import block_registry


block_registry.register_block(
    'heading',
    CharBlock(
        classname="full title",
        label='Heading',
        icon='title',
        template='wagtail_stacks/heading.html'
    )
)

block_registry.register_block(
    'paragraph',
    RichTextBlock(
        icon='form',
        label='Rich Text',
        template='wagtail_stacks/rich_text_block.html'
    )
)
